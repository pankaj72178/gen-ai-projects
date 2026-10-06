# Gen AI Projects

Four small, self-contained examples of building LLM agents with [LangChain](https://www.langchain.com/) and [Groq](https://groq.com/). Each project lives in its own folder and runs as a single Python script.

| # | Project | Folder | What it shows |
|---|---------|--------|---------------|
| 1 | Basic agent | [1st_agent/](1st_agent/) | An agent with one web-search tool |
| 2 | Agent with tools | [2_agent_with_tools/](2_agent_with_tools/) | An agent choosing between several custom tools |
| 3 | Reasoning agent | [3_reasoning_agent/](3_reasoning_agent/) | Step-by-step reasoning with no tools |
| 4 | Multimodal | [4_multimodal/](4_multimodal/) | Sending images to a vision model and getting JSON back |

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Groq API key](https://console.groq.com/keys) (needed by all projects)
- A [SerpAPI key](https://serpapi.com/manage-api-key) (needed by project 1 only)

## Installation

All four projects share one set of dependencies, declared in [pyproject.toml](pyproject.toml):

```toml
dependencies = [
    "google-search-results>=2.4.2",
    "langchain>=1.4.3",
    "langchain-community>=0.4.2",
    "langchain-groq>=1.1.3",
    "python-dotenv>=1.2.4",
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
```

Each script calls `load_dotenv()` to read these values. Keep `.env` out of version control, since it holds your secret keys.

## Running the projects

Run every command from the project root. With uv:

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
├── src/gen_ai_projects/
├── .env                 # your API keys (create this yourself)
├── .python-version
├── pyproject.toml       # dependencies
└── uv.lock              # locked versions
```

## Troubleshooting

- **`GROQ_API_KEY` or `SERPAPI_API_KEY` error:** check that `.env` is in the project root and that you run the script from there.
- **`ModuleNotFoundError`:** the dependencies are not installed in the active environment. Run `uv sync`, or activate `.venv` before using `python`.
- **Model not found error from Groq:** the model names are set near the top of each script (`ChatGroq(model=...)`). Groq retires models over time, so swap in a current one from the [Groq model list](https://console.groq.com/docs/models).
