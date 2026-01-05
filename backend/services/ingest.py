# services/ingest.py
import re
from bs4 import BeautifulSoup  # <-- add this
from db import SessionLocal
from models import RawDocument
from milvus.service import insert_embeddings

def clean_text(text: str) -> str:
    """Remove HTML tags, scripts, and excessive whitespace."""
    soup = BeautifulSoup(text, "html.parser")

    # Remove script/style
    for script in soup(["script", "style"]):
        script.extract()

    cleaned = soup.get_text(separator=" ")
    cleaned = re.sub(r"\s+", " ", cleaned)  # normalize whitespace
    return cleaned.strip()


def split_markdown(text: str, max_length: int = 500):
    """Split text by paragraphs/headings but keep chunks under max_length."""
    paragraphs = re.split(r"\n\s*\n", text.strip())  # split by blank lines
    chunks, current = [], ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_length:
            current += ("\n\n" + para if current else para)
        else:
            chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks


from utils.cleaner import clean_text

def process_and_ingest(competitor_id: int, text: str, chunk_size: int = 500):
    db = SessionLocal()
    try:
        # Clean before saving
        cleaned_text = clean_text(text)

        raw = RawDocument(competitor_id=competitor_id, text=cleaned_text)
        db.add(raw)
        db.commit()
        db.refresh(raw)

        chunks = split_markdown(cleaned_text, chunk_size)
        insert_embeddings(competitor_id, raw.id, chunks)

        print(f"[INGEST] Competitor {competitor_id}, RawDoc {raw.id}, Chunks {len(chunks)}")

        return raw.id, len(chunks)
    finally:
        db.close()

