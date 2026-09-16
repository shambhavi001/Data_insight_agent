[README.md](https://github.com/user-attachments/files/32278099/README.md)
# PySpark Data Insights Agent

A Google ADK analytics agent that answers natural-language questions about the restaurant Tips dataset. The agent uses PySpark for aggregations, Gemini for a short narrated summary, Matplotlib for chart generation, and simple in-memory storage for the latest question.

## Features

- Loads the public `tips.csv` dataset from the Seaborn data repository
- Converts the Pandas DataFrame into a PySpark DataFrame
- Accepts natural-language analytics questions
- Performs supported PySpark aggregations
- Generates a bar chart as a PNG file
- Produces 3 to 4 simple insights using Gemini
- Stores the latest question in simple in-memory storage
- Runs as a Google ADK command-line agent

## Supported Questions

The current agent supports questions such as:

1. `Which day has the highest total tips?`
2. `Show the average bill by day.`
3. `Compare the average tips for smokers and non-smokers.`

Questions outside these patterns return a supported-question message.

## Project Structure

```text
Data_insight_agent/
├── __init__.py
├── agent.py
├── .env
└── README.md
```

The generated chart is saved at:

```text
/content/Data_insight_agent/insights_chart.png
```

## Technologies Used

- Python
- Google Agent Development Kit (ADK)
- Gemini API
- PySpark
- Pandas
- Matplotlib
- Google Colab

## Dataset

The project uses the Seaborn restaurant Tips dataset:

```text
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv
```

Dataset columns:

- `total_bill`
- `tip`
- `sex`
- `smoker`
- `day`
- `time`
- `size`

## Setup in Google Colab

### 1. Install the required packages

```bash
pip install google-adk pyspark pandas matplotlib google-genai
```

### 2. Create the environment file

Create a `.env` file inside the `Data_insight_agent` directory:

```text
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

Do not commit the `.env` file to GitHub.

### 3. Create `__init__.py`

Add the following line:

```python
from . import agent
```

### 4. Run the agent

Run the command from the `/content` parent directory:

```bash
cd /content
adk run Data_insight_agent
```

## Sample Q&A

```text
User: Which day has the highest total tips?

Agent: Calls insight_tool, calculates total tips grouped by day with
PySpark, generates a chart, and returns a narrated summary.
```

```text
User: Show the average bill by day.

Agent: Calculates the average total bill for each day, sorts the
results, generates a chart, and returns the insight summary.
```

```text
User: Compare the average tips for smokers and non-smokers.

Agent: Groups the dataset by smoker status, calculates average tips,
generates a comparison chart, and returns a narrated summary.
```

## How It Works

```text
Natural-language question
        ↓
Google ADK agent
        ↓
insight_tool()
        ↓
PySpark aggregation
        ↓
Pandas conversion
        ↓
Matplotlib chart
        ↓
Gemini narrated summary
```

## Security

The Gemini API key is read from the `GOOGLE_API_KEY` environment variable. Add the following files to `.gitignore`:

```text
.env
__pycache__/
*.pyc
insights_chart.png
```





