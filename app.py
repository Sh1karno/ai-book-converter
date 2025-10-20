import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import fitz  # PyMuPDF
from ebooklib import epub

app = FastAPI()


def pdf_to_epub(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    book = epub.EpubBook()
    book.set_identifier("id0")
    book.set_title("Converted PDF")
    book.set_language("en")

    chapters = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text()
        chapter = epub.EpubHtml(
            title=f"Page {i + 1}", file_name=f"page_{i + 1}.xhtml"
        )
        chapter.set_content(f"<h1>Page {i + 1}</h1><p>{text}</p>")
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = chapters
    book.spine = ["nav"] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    result = io.BytesIO()
    epub.write_epub(result, book)
    result.seek(0)
    return result


@app.post("/convert")
async def convert(pdf: UploadFile = File(...)):
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type")
    epub_data = pdf_to_epub(await pdf.read())
    return StreamingResponse(
        epub_data,
        media_type="application/epub+zip",
        headers={"Content-Disposition": "attachment; filename=output.epub"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

