import json
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from data import SALES_DATA

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a: list, b: list) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def build_index() -> list[dict]:
    print("Building embeddings index...")
    index = []
    for record in SALES_DATA:
        text = (
            f"{record['month']} sales: {record['product']} "
            f"generated ${record['revenue']} revenue with {record['units']} units sold"
        )
        embedding = get_embedding(text)
        index.append({
            "record": record,
            "text": text,
            "embedding": embedding
        })
    print(f"Index built: {len(index)} records")
    return index

def semantic_search(query: str, index: list, top_k: int = 3) -> list[dict]:
    query_embedding = get_embedding(query)
    results = []
    for item in index:
        score = cosine_similarity(query_embedding, item["embedding"])
        results.append({
            "record": item["record"],
            "text": item["text"],
            "score": round(score, 4)
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    index = build_index()

    queries = [
        "best performing month",
        "cheap products with few sales",
        "automation tools revenue",
        "API related income"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = semantic_search(query, index)
        for r in results:
            print(f". [{r['score']}] {r['text']}")