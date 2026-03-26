# Sales Agent

Conversational agent that answers natural language questions about sales data
using OpenAI function calling. 

The model never guesses or estimates - it calls real Python functions to retrieve
data and formulates answers from actual results.

## Features
- Ask questions in plain English about sales performance
- Agent selects the right function automatically based on the question
- Chains multiple function calls when needed to enrich the answer
- Maintains conversation history across multiple turns
- Structured JSON responses with strict JSON Schema validation
- Streaming support: responses appear token by token
- Semantic search with embeddings: find records by meaning, not exact words
- RAG pipeline: model answers using only retrieved context, never hallucinated data
 

## Example interaction
**Conversational with history:**
```
You: How much did we sell in March?
Agent: In March, total revenue was $6,700 across 11 units...
 
You: And in January?
Agent: In January, total revenue was $2,500 across 6 units...
 
You: Which of those two months was better?
Agent: March was significantly better, with $4,200 more in revenue...
```

**Function calling chain:**
``` 
You Compare January and March
Agent thinking...
  [calling compare_months with {'month_a': 'January', 'month_b': 'March'}]
  [calling get_sales_by_month with {'month': 'January'}]
  [calling get_sales_by_month with {'month': 'March'}]
Agent: March outperformed January significantly — $6,700 vs $2,500, a 168% increase...
```

**Structured JSON output:**
```
You: json: What was the top product in March?
Agent (JSON): {
  "answer": "The top product in March was API Integration, generating $3,100.",
  "data_used": ["get_top_product"],
  "confidence": "high",
  "follow_up_suggestions": [...]
}
```

**Semantic search:**
```
Query: 'API related income'
  [0.5515] March sales: API Integration generated $3100 revenue with 3 units sold
  [0.5511] April sales: API Integration generated $2800 revenue with 3 units sold
```

## Available tools
| Function | Description |
|----------|-------------|
| `get_sales_by_month` | Total revenue and units sold for a specific month |
| `get_top_product` | Best-selling product by revenue, optionally filtered by month |
| `compare_months` | Revenue comparison between two months with percentage change |
| `get_total_revenue` | Total revenue and units across all months |

## How to use
1. Clone this repository
2. Install dependencies
```
pip install -r requirements.txt
```
3. Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```
4. Run the conversational agent:
```
python3 main.py
```
5. Run the RAG pipeline:
```
python3 rag.py
```
6. Run semantic search standalone:
```
python3 embeddings.py
```

## Input modes in main.py
| Prefix | Mode | Example |
|--------|------|---------|
| *(none)* | Conversational with history | `How much did we sell in March?` |
| `json:` | Structured JSON output | `json: What was the top product?` |
| `stream:` | Streaming token by token | `stream: Give me a full analysis` |

## Project structure
```
sales-agent/
├── main.py         # Conversation loop with mode routing
├── agent.py        # Function calling loop, tool definitions, streaming, structured output
├── tools.py        # Real functions the model can call
├── data.py         # Sales data
├── embeddings.py   # Embedding generation and semantic search
└── rag.py          # RAG pipeline: retrieve context, then generate answer
```

## Tech stacks
- Python 3
- OpenAI API (gpt-4o-mini, text-embedding-3-small)
- numpy
- python-dotenv

## Notes
- **Function calling over prompting**: The model doesn't generate numbers — it calls real functions and formats the results. This eliminates hallucination entirely for data questions.
- **Tool loop**: The agent keeps calling functions until `finish_reason == "stop"`, allowing multi-step reasoning in a single user turn.
- **JSON Schema over json_object**: Using `strict: True` with a full schema guarantees field types and values — `confidence` can only be `high`, `medium`, or `low`, never anything else.
- **Streaming**: Tool calls are resolved first in a standard loop, then the final answer is streamed token by token. Mixing streaming and tool calls in a single pass adds complexity without benefit for most use cases.
- **RAG limitations**: Response quality depends on which chunks are retrieved. If the index is small and `top_k` is low, the model may answer with incomplete context. In production this is addressed by improving chunk text quality, increasing `top_k`, or splitting long documents into smaller overlapping chunks.
- **Embeddings index**: The index is rebuilt on every run. In production it would be persisted to disk to avoid recalculating embeddings on each execution — especially important when indexing hundreds or thousands of documents.
- **In-memory data**: Intentional for simplicity. Production version would connect to a database or external API.