# ai-book-converter

This project provides a simple web application in Python that converts PDF files to EPUB format.

## Installation

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the FastAPI application with Uvicorn and send a PDF to the `/convert` endpoint.

```bash
uvicorn app:app --reload
```

You can convert a PDF using `curl`:

```bash
curl -F pdf=@example.pdf http://localhost:5000/convert -o output.epub
```

The resulting `output.epub` will contain the text from the uploaded PDF.

