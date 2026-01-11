import re
from bs4 import BeautifulSoup

def clean_text(raw_html: str) -> str:
    """Clean up raw scraped HTML/text before passing to retriever/generator."""
    if not raw_html:
        return ""

    # 1. Remove HTML tags/scripts/styles
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.extract()
    text = soup.get_text(separator=" ")

    # 2. Remove markdown artifacts
    text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)   # images
    text = re.sub(r"\[.*?\]\(.*?\)", " ", text)    # links
    text = re.sub(r"[#*>`]", " ", text)

    # 3. Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def deduplicate_chunks(chunks: list[str]) -> list[str]:
    """Remove near-duplicate chunks (same text repeating)."""
    seen = set()
    unique = []
    for c in chunks:
        cleaned = c.strip()
        if cleaned and cleaned not in seen:
            unique.append(cleaned)
            seen.add(cleaned)
    return unique
