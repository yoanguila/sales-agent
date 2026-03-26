# Sales Agent

Conversational agent that answers natural language questions about sales data
using OpenAI function calling. 

The model never guesses or estimates - it calls real Python functions to retrieve
data and formulates answers from actual results.

## Features
- Ask questions in plain English about sales performance
- Agent selects the right function automatically based on the question
- Chains multiple function calls when needed to enrich the answer
- Returns structured data from real sources, never hallucinated numbers
- Maintains conversation history across multiple turns
- Structured JSON responses with strict JSON Schema validation
- Multi-step reasoning: chains multiple function calls in a single turn
- Easily extensible: add new functions and the agent picks them automatically

## Example interaction
``` 
You Compare January and March
Agent thinking...
  [calling compare_months with {'month_a': 'January', 'month_b': 'March'}]
  [calling get_sales_by_month with {'month': 'January'}]
  [calling get_sales_by_month with {'month': 'March'}]
Agent: March outperformed January significantly — $6,700 vs $2,500, a 168% increase...
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
4. Run the agent:
```
python3 main.py
```
5. Ask questions in plain English. Type `exit` to quit.

## Example questions
```
How much did we sell in March?
What was the top product in February?
Compare January and March
What was our total revenue?
```

## Tech stacks
- Python 3
- OpenAI API (gpt-4o-mini)
- python-dotenv

## Project structure
```
sales-agent/
├── main.py      # Conversation loop
├── agent.py     # Function calling loop and tool definitions
├── tools.py     # Real functions the model can call
└── data.py      # Sales data
```

## Notes
- **Function calling over prompting**: The model doesn't generate numbers - it calls
real functions and formats the results. This eliminates hallucination entirely for 
data questions.
- **Tool loop**: The agent keeps calling functions until `finish_reason == "stop"`, allowing multi-step reasoning in a single user turn.
- **Extensible by design**: Adding a new capability means writing a Python function and adding its definition to `TOOLS`. No changes to the agent logic needed.
- **In-memory data**: Intentional for simplicity. Production version would connect to a database or external API.