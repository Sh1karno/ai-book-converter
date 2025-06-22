import io
from flask import Flask, request, send_file, jsonify
import fitz  # PyMuPDF
from ebooklib import epub

app = Flask(__name__)


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


@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400
    uploaded = request.files["pdf"]
    epub_data = pdf_to_epub(uploaded.read())
    return send_file(
        epub_data,
        as_attachment=True,
        download_name="output.epub",
        mimetype="application/epub+zip",
    )


if __name__ == "__main__":
    app.run(debug=True)

