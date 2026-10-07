# Gen AI Projects

Eight small, self-contained examples of building, evaluating and guarding LLM agents with [LangChain](https://www.langchain.com/) and [Groq](https://groq.com/). Each project lives in its own folder.

| # | Project | Folder | What it shows |
|---|---------|--------|---------------|
| 1 | Basic agent | [1st_agent/](1st_agent/) | An agent with one web-search tool |
| 2 | Agent with tools | [2_agent_with_tools/](2_agent_with_tools/) | An agent choosing between several custom tools |
| 3 | Reasoning agent | [3_reasoning_agent/](3_reasoning_agent/) | Step-by-step reasoning with no tools |
| 4 | Multimodal | [4_multimodal/](4_multimodal/) | Sending images to a vision model and getting JSON back |
| 5 | Functional evals | [5_evals_func/](5_evals_func/) | Scoring an agent's answers against a LangSmith dataset with embedding similarity |
| 6 | LLM-as-judge evals | [6_evals_func_llm_judge/](6_evals_func_llm_judge/) | Scoring the same agent with a second model as the judge |
| 7 | Operational metrics | [7_eval_op_metrics/](7_eval_op_metrics/) | Re-running the eval on a different model to compare latency, tokens and cost |
| 8 | Guardrails | [8_guardrails/](8_guardrails/) | Redacting, masking and blocking sensitive data with PII middleware |

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Groq API key](https://console.groq.com/keys) (needed by all projects)
- A [SerpAPI key](https://serpapi.com/manage-api-key) (needed by project 1 only)
- A [LangSmith API key](https://smith.langchain.com/settings) (needed by projects 5, 6 and 7)

## Installation

All projects share one set of dependencies, declared in [pyproject.toml](pyproject.toml):

```toml
dependencies = [
    "google-search-results>=2.4.2",
    "langchain>=1.4.3",
    "langchain-community>=0.4.2",
    "langchain-groq>=1.1.3",
    "langsmith>=0.14.4",
    "numpy>=2.5.3",
    "python-dotenv>=1.2.4",
    "sentence-transformers>=6.1.0",
    "yfinance>=1.7.0",
]
```

### Option A: uv (recommended)

1. Install uv if you don't have it:

   ```bash
   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. From the project root, install everything in `pyproject.toml`:

   ```bash
   uv sync
   ```

   This creates a `.venv` folder, installs the Python version pinned in `.python-version`, and installs the exact package versions recorded in `uv.lock`.

To add a new dependency later, use `uv add <package>`. It updates `pyproject.toml` and `uv.lock` together.

### Option B: pip

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install .
```

`pip install .` reads the dependency list from `pyproject.toml`. Building the project this way needs pip 23 or newer.

## Set up API keys

Create a file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SERPAPI_API_KEY=your_serpapi_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
```

Each script calls `load_dotenv()` to read these values. Keep `.env` out of version control, since it holds your secret keys.

## Running the projects

Run every command from the project root, except projects 5, 6 and 7, which run from inside their own folder. With uv:

```bash
uv run <path-to-script>
```

With pip, activate the virtual environment first, then use `python <path-to-script>`.

### 1. Basic agent

```bash
uv run 1st_agent/basic_agent.py
```

A news-reporter agent. It has one tool, `search_news`, which searches Google News for the past 24 hours through SerpAPI. The agent is asked for the latest US political news and replies with a three-line summary, the date and the source URL.

Needs: `GROQ_API_KEY`, `SERPAPI_API_KEY`

### 2. Agent with tools

```bash
uv run 2_agent_with_tools/agent_with_tools.py
```

A finance agent with two tools, which picks the right one for the question:

- `get_stock_price` looks up the live price of a public ticker with `yfinance`.
- `get_market_valuation_of_private_company` returns a valuation for a private company from a small hard-coded table (SpaceX, Stripe, Airbnb). The numbers are placeholders, not real data.

The sample question is "What is the valuation of SpaceX?".

Needs: `GROQ_API_KEY`

### 3. Reasoning agent

```bash
uv run 3_reasoning_agent/reasoning_agent.py
```

An agent with no tools, prompted to number each reasoning step and write formulas in plain text. The sample question is how long a cheetah would take to travel from New Delhi to Mumbai.

Needs: `GROQ_API_KEY`

### 4. Multimodal

Two scripts:

```bash
uv run 4_multimodal/multimodal_1.py
uv run 4_multimodal/multimodal_2.py
```

- `multimodal_1.py` asks the model to name the bird in a photo. The prompt ends where the image link should go, so add an image URL to the prompt before running it.
- `multimodal_2.py` reads the three clothing photos in [4_multimodal/images/](4_multimodal/images/), sends them to a vision model as base64 data URLs, and asks for one JSON record per image with `item_name`, `color`, `gender` and `age_category`. The script then fills in `item_code` itself using `get_item_code`, and prints the result:

  ```json
  [
    {
      "item_name": "saree",
      "item_code": "ITM001",
      "color": "red",
      "gender": "female",
      "age_category": "adult"
    }
  ]
  ```

Needs: `GROQ_API_KEY`

### 5. Functional evals

```bash
cd 5_evals_func
uv run func_eval.py
```

Projects 5, 6 and 7 import `inventory_agent.py` and `utils.py` from their own folder, so run them from inside that folder.

`inventory_agent.py` is a small inventory assistant with one tool, `inventory_tool`, backed by a hard-coded stock table. `func_eval.py` creates a LangSmith dataset named `inventorydata` (five questions with expected answers) if it does not exist yet, runs the agent on each question, and scores every answer with `semantic_match`: the cosine similarity between the expected and actual answer, computed with the `all-MiniLM-L6-v2` sentence-transformers model. The first run downloads that model. Results appear as an experiment in LangSmith.

Needs: `GROQ_API_KEY`, `LANGSMITH_API_KEY`

### 6. LLM-as-judge evals

```bash
cd 6_evals_func_llm_judge
uv run func_eval_llm_judge.py
```

The same agent and dataset as project 5, but the evaluator is a second model (`openai/gpt-oss-20b`). It is shown the question, the expected answer and the actual answer, and returns a correctness score between 0 and 1 as JSON.

Needs: `GROQ_API_KEY`, `LANGSMITH_API_KEY`

### 7. Operational metrics

```bash
cd 7_eval_op_metrics
uv run func_eval.py
```

The same eval as project 5 with the agent switched to `openai/gpt-oss-20b`. Open the two experiments side by side in LangSmith to compare latency, token usage and cost alongside the `semantic_match` score.

Needs: `GROQ_API_KEY`, `LANGSMITH_API_KEY`

### 8. Guardrails

```bash
uv run 8_guardrails/guardrails_1.py
uv run 8_guardrails/guardrails_2.py
```

- `guardrails_1.py` is a customer-service agent whose tool returns an email address and a credit card number. `PIIMiddleware` redacts the email and masks the card before they reach the model or the user, so the reply shows `[REDACTED_EMAIL]` and `****-****-****-1111`.
- `guardrails_2.py` is an interactive docs assistant for three made-up languages. `PIIMiddleware` with a custom regex and `strategy="block"` rejects any message containing an API key of the form `sk-` followed by 32 letters or digits. Type `quit` to exit.

Needs: `GROQ_API_KEY`

## Project structure

```
gen-ai-projects/
├── 1st_agent/
│   └── basic_agent.py
├── 2_agent_with_tools/
│   └── agent_with_tools.py
├── 3_reasoning_agent/
│   └── reasoning_agent.py
├── 4_multimodal/
│   ├── images/
│   ├── multimodal_1.py
│   └── multimodal_2.py
├── 5_evals_func/
│   ├── func_eval.py
│   ├── inventory_agent.py
│   └── utils.py
├── 6_evals_func_llm_judge/
│   ├── func_eval_llm_judge.py
│   ├── inventory_agent.py
│   └── utils.py
├── 7_eval_op_metrics/
│   ├── func_eval.py
│   ├── inventory_agent.py
│   └── utils.py
├── 8_guardrails/
│   ├── guardrails_1.py
│   └── guardrails_2.py
├── src/gen_ai_projects/
├── .env                 # your API keys (create this yourself)
├── .python-version
├── pyproject.toml       # dependencies
└── uv.lock              # locked versions
```

## Troubleshooting

- **`GROQ_API_KEY` or `SERPAPI_API_KEY` error:** check that `.env` is in the project root and that you run the script from there.
- **`LangSmithAuthError` / 401 Invalid token:** `LANGSMITH_API_KEY` is missing from `.env` or is wrong. Projects 5, 6 and 7 cannot run without it.
- **`ModuleNotFoundError: inventory_agent` or `utils`:** run projects 5, 6 and 7 from inside their own folder.
- **`ModuleNotFoundError`:** the dependencies are not installed in the active environment. Run `uv sync`, or activate `.venv` before using `python`.
- **Model not found error from Groq:** the model names are set near the top of each script (`ChatGroq(model=...)`). Groq retires models over time, so swap in a current one from the [Groq model list](https://console.groq.com/docs/models).
