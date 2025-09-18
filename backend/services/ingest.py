from models import RawDocument
from milvus.service import insert_embeddings
from db import SessionLocal
import re
import datetime



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

def process_and_ingest(competitor_id: int, text: str, chunk_size: int = 500):
    db = SessionLocal()
    try:
        raw = RawDocument(competitor_id=competitor_id, text=text, scraped_at = datetime.datetime.now())
        db.add(raw)
        db.commit()
        db.refresh(raw)

        chunks = split_markdown(text, chunk_size)
        insert_embeddings(competitor_id, raw.id, chunks)

        return raw.id, len(chunks)
    finally:
        db.close()



