import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import os

from ingestion.pdf_loader import load_pdf_with_metadata
from ingestion.xml_loader import load_pubmed_xml
from ingestion.chunker import chunk_documents

RAW_PDF_DIR = "data/raw/pdf"
RAW_XML_DIR = "data/raw/xml"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

documents = []

#Load PDFs
for file in os.listdir(RAW_PDF_DIR):
    if file.endswith(".pdf"):
        path = os.path.join(RAW_PDF_DIR, file)
        source = file.replace(".pdf", "").replace("_", " ").title()
        print(f"Reading PDF: {file}")
        documents.extend(load_pdf_with_metadata(path, source))

#Load XML
for file in os.listdir(RAW_XML_DIR):
    if file.endswith(".xml"):
        path = os.path.join(RAW_XML_DIR, file)
        print(f"Reading XML: {file}")
        documents.extend(load_pubmed_xml(path))

#Save documents
with open(f"{PROCESSED_DIR}/documents.json", "w") as f:
    json.dump(documents, f, indent=2)

print(f"Saved documents.json ({len(documents)} records)")

#Chunk documents
chunks = chunk_documents(documents)

with open(f"{PROCESSED_DIR}/chunks.json", "w") as f:
    json.dump(chunks, f, indent=2)

print(f"Saved chunks.json ({len(chunks)} chunks)")
print("Processing completed successfully")
