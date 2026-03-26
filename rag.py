import os
from dotenv import load_dotenv
from openai import OpenAI
from embeddings import build_index, semantic_search

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(query: str, index: list) -> str:
    # Step 1: retrieve relevant records
    results = semantic_search(query, index, top_k=4)

    # Step 2: build context from retrieved records
    context = "\n".join([r["text"] for r in results])

    # Step 3: ask the model using only the retrieved context
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sales analyst. Answer the user's question using only "
                    "the data provided below. If the answer is not in the data, say so.\n\n"
                    f"Data:\n{context}"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    index = build_index()

    questions = build_index()

    questions = [
        "Which product consistently generates the most revenue?",
        "Was there any month where Telegram Bot outperformed Web Scraper?",
        "What can you tell me about PDF Extractor performance?",
    ]

    for question in questions:
        print(f"\nQ: {question}")
        answer = ask(question, index)
        print(f"A: {answer}")