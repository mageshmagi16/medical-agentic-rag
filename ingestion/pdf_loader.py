import fitz

def load_pdf_with_metadata(path: str, source: str):
    doc = fitz.open(path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "text": text,
                "metadata": {
                    "source": source,
                    "page": i + 1,
                    "type": "pdf"
                }
            })
    return pages

