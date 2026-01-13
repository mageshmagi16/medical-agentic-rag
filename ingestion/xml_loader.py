import xml.etree.ElementTree as ET

def load_pubmed_xml(path):
    documents = []

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as e:
        print(f" Skipping invalid XML: {path}")
        print(f"    Reason: {e}")
        return documents

    for article in root.iter("PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        abstract_elems = article.findall(".//AbstractText")

        title = title_elem.text.strip() if title_elem is not None else ""

        abstract_texts = []
        for ab in abstract_elems:
            if ab.text:
                abstract_texts.append(ab.text.strip())

        full_text = " ".join([title] + abstract_texts)

        if full_text:
            documents.append({
                "text": full_text,
                "metadata": {
                    "source": "PubMed",
                    "type": "xml",
                    "file": path
                }
            })

    return documents
