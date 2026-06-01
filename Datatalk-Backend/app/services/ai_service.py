from fastapi import HTTPException
from ..core.config import settings
import google.generativeai as genai
import json
def create_prompt(summary, question):
    prompt = f"""
    You are an expert data analyst engineer with years of experience analyzing CSV datasets. 
    You carefully examine data, find patterns, and give precise, insightful answers.
    Always analyze the data thoroughly before answering.

    Data Summary:
    {summary}

    Question: {question}

    Chart Rules:
    - If the question is about comparison then use bar
    - If the question is about trend over time then use line
    - If the question is about part of a whole then use pie
    - If there is no need for chart then set charts to null

    IMPORTANT: Return answers in the exact format below. No extra text, no markdown, no explanation outside the JSON.
    Return only this JSON format:
    {{
        "answer": "your answer here",
        "charts": {{
            "type": "bar or line or pie",
            "labels": ["label1", "label2"],
            "values": [200, 300]
        }}
    }}

    Remember: Return only JSON. No extra text!
    If the question is not related to the dataset
    return {{"answer": "This question is not related to the dataset", "charts": null}}

    """
    return prompt

from groq import Groq

def ask_gemini(prompt):
    try:
        client = Groq(api_key=settings.API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        answer = data["answer"]
        charts = data.get("charts", None)
        return answer, charts
    except Exception as e:
        print(f"GROQ ERROR: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")