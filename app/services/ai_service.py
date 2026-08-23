import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY")) 

def ask_groq(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"} 
    )
    
    raw = response.choices[0].message.content.strip()
    
    if raw.startswith("```json"):
        raw = raw[7:]
    elif raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
        
    return json.loads(raw.strip())


def generate_query_plan(metadata: list, question: str, filepath: str) -> dict:
    prompt = f"""
        You are a Lead Data Analyst and SQL Engineer. Your objective is to translate user natural language questions into precise DuckDB SQL queries and determine the optimal chart configuration.

        ### Dataset Metadata & Schema:
        {metadata}

        ### Target Filepath (Use as the table name in SQL):
        '{filepath}'

        ### User Question:
        {question}

        ---

        ### SQL Generation Rules:
        1. **Target Table:** Always query directly from '{filepath}'.
        2. **Column Quoting:** Wrap any column name with spaces, hyphens, or special characters in double quotes (e.g., "Order ID", "Year-Month", "Order Date").
        3. **Aggregations & Aliases:** When aggregating (SUM, AVG, COUNT, MIN, MAX), always assign explicit column aliases (e.g., `SUM("Amount") AS total_amount`).
        4. **Time-Series / Trends:** When grouping by date/month (e.g., "Year-Month", "Order Date"), always include an `ORDER BY` clause to ensure chronological ordering.
        5. **Categorical Comparisons:** When comparing categories, sort by the aggregated metric descending and apply `LIMIT 10` unless the user asks for all.
        6. **Null Handling:** Filter out null values when aggregating if necessary (e.g., `WHERE "Amount" IS NOT NULL`).

        ---

        ### Chart Selection Rules:
        - **Bar Chart (`"bar"`):** Use when comparing discrete categories, rankings, top/bottom performers, or distributions across items.
        - `x_axis`: The categorical column name or alias (e.g., "Category", "State").
        - `y_axis`: The numerical aggregated column name or alias (e.g., "total_amount").
        - **Line Chart (`"line"`):** Use when analyzing trends over time, chronological movements, or continuous sequential metrics.
        - `x_axis`: The date, year, or period column name (e.g., "Year-Month", "Order Date").
        - `y_axis`: The numerical aggregated column name (e.g., "monthly_profit").
        - **Pie Chart (`"pie"`):** Use strictly when showing parts of a whole, percentage share, or proportion across fewer than 7 categories.
        - `x_axis`: The label/slice category column name (e.g., "PaymentMode").
        - `y_axis`: The numerical value column representing slice size (e.g., "count").
        - **No Chart (`null`):** Use when the query produces a single scalar value (e.g., "What was total revenue?"), a detailed raw record lookup, a greeting, or an unanswerable question.
        - Set `"type": null`, `"x_axis": null`, `"y_axis": null`.

        ---

        ### Edge Cases & Handling:
        1. **Greetings & Casual Input:** If the user sends a greeting (e.g., "hi", "hello", "good morning"), set `sql_query` to `null`, `chart` fields to `null`, and write a polite, friendly greeting in `explanation`.
        2. **Out of Scope Questions:** If the user query is unrelated to the dataset schema, set `sql_query` to `null`, `chart` fields to `null`, and set `explanation` to `"This question cannot be answered using the provided dataset schema."`.

        ---

        ### Output Format:
        Return ONLY valid JSON matching this exact structure with no markdown wrapping outside the JSON:

        {{
            "sql_query": "SELECT ... FROM '{filepath}' ...",
            "chart": {{
                "type": "bar" | "line" | "pie" | null,
                "x_axis": "column_name_or_alias_for_labels",
                "y_axis": "column_name_or_alias_for_values"
            }},
            "explanation": "Clear, concise natural language explanation of the generated analysis."
        }}
    """
    
    return ask_groq(prompt)