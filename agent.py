import pandas as pd
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, desc

from google import genai
from google.adk.agents import Agent

import os


# Load API key from the .env file
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# Load tips dataset
url = (
    "https://raw.githubusercontent.com/"
    "mwaskom/seaborn-data/master/tips.csv"
)

pdf = pd.read_csv(url)


# Create Spark session
spark = (
    SparkSession.builder
    .appName("DataInsightAgent")
    .getOrCreate()
)


# Convert Pandas DataFrame to PySpark DataFrame
df = spark.createDataFrame(pdf)


# Simple memory
memory = {}


def save_question(question: str):
    memory["last_question"] = question


def get_last_question():
    return memory.get(
        "last_question",
        "No previous question"
    )


# PySpark analytics function
def analyze_data(question: str):

    q = question.lower()

    if "total tips" in q or "highest total tips" in q:

        result = (
            df.groupBy("day")
            .agg(
                sum("tip").alias("total_tip")
            )
            .orderBy(
                desc("total_tip")
            )
        )

        return result

    elif "average bill" in q:

        result = (
            df.groupBy("day")
            .agg(
                avg("total_bill").alias("avg_bill")
            )
            .orderBy(
                desc("avg_bill")
            )
        )

        return result

    elif "smoker" in q:

        result = (
            df.groupBy("smoker")
            .agg(
                avg("tip").alias("avg_tip")
            )
            .orderBy(
                desc("avg_tip")
            )
        )

        return result

    else:

        return None


# Generate narrated summary using Gemini
def generate_summary(question: str, result_pd):

    prompt = f"""
User Question:
{question}

Analysis Result:
{result_pd.to_string(index=False)}

Write 3 to 4 simple business insights.
Use only the result provided.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text


# Generate chart
def generate_chart(question: str, result_pd):

    columns = result_pd.columns

    x_col = columns[0]
    y_col = columns[1]

    plt.figure(figsize=(8, 5))

    plt.bar(
        result_pd[x_col],
        result_pd[y_col]
    )

    plt.title(question)
    plt.xlabel(x_col)
    plt.ylabel(y_col)

    plt.tight_layout()

    chart_path = (
        "/content/Data_insight_agent/"
        "insights_chart.png"
    )

    plt.savefig(chart_path)
    plt.close()

    return chart_path


# Final tool used by ADK agent
def insight_tool(question: str):

    save_question(question)

    result = analyze_data(question)

    if result is None:

        return {
            "status": "error",
            "message": (
                "Question not supported. "
                "Ask about total tips, "
                "average bill, or smokers."
            )
        }

    result_pd = result.toPandas()

    chart_path = generate_chart(
        question,
        result_pd
    )

    summary = generate_summary(
        question,
        result_pd
    )

    return {
        "status": "success",
        "summary": summary,
        "chart_path": chart_path,
        "last_question": get_last_question()
    }


# Create ADK agent
root_agent = Agent(
    name="data_insight_agent",

    model="gemini-flash-latest",

    description="Tips analytics agent",

    instruction="""
Use insight_tool for analytical questions
about the tips dataset.

Always call insight_tool before answering.

The tool supports:
1. Total tips by day
2. Average bill by day
3. Average tip by smoker status

Use only the result returned by the tool.
""",

    tools=[insight_tool]
)
