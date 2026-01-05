from pymilvus import Collection
from milvus.client import ensure_collection

coll: Collection = ensure_collection()

# Check for Marvel specifically
results = coll.query(
    expr="competitor_id == 19",   # Marvel’s ID
    output_fields=["competitor_id", "doc_id", "chunk_id"]
)

print(f"Found {len(results)} vectors for Marvel (competitor_id=19)")
for r in results:
    print(r)
