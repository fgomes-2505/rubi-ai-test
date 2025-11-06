from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import io, json
from ingestion.models import ExtractedData


load_dotenv()

def extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def process_pdf_with_agent(pdf_file) -> dict:
    pdf_bytes = pdf_file.read()
    text = extract_pdf_text(pdf_bytes)

    model = ChatOpenAI(model="gpt-4o-mini")

    prompt = f"""
    You are a data extraction assistant.
    From the following PDF text, extract and return a JSON with:
    - industry
    - company_name
    - revenue
    - ebitda
    - customer_concentration
    - market_size
    1. Return only the JSON object (don't add backticks). It's mandatory
    2. If any field is missing, set its value to null
    3. Follow this data type:
       - industry: string
       - company_name: string
       - revenue: float
       - ebitda: float
       - customer_concentration: float
       - market_size: float
    4. Consider the following example format:
    {{
        "industry": "Retail",
        "company_name": "ABC Corp",
        "revenue": 1500000.0,
        "ebitda": 250000.0,
        "customer_concentration": 30.5,
        "market_size": 5000000.0
    }}
    5. For numerical values, verify if they are in thousands or millions based on the context and convert them accordingly. (e.g., 1.5M should be 1500000.0)

    PDF TEXT:
    {text}
    """

    response = model.invoke(prompt)

    try:
        return json.loads(response.content)
    except Exception:
        raise ValueError("Failed to parse JSON from model response")


def suggest_companies_with_agent(pdf_file) -> dict:
    pdf_bytes = pdf_file.read()
    text = extract_pdf_text(pdf_bytes)
    companies = list(ExtractedData.objects.all().values())

    model = ChatOpenAI(model="gpt-5-mini")

    system_prompt = f"""
        You are an investment analysis assistant.

        Given a user's investment criteria and a list of companies (with fields:
        industry, revenue, ebitda, customer_concentration, and market_size),
        you must rank which 5 companies best match the user's criteria.

        Use this weighted scoring logic for your reasoning:

        - Revenue similarity: 40%
        - EBITDA similarity: 30%
        - Market size similarity: 20%
        - Customer concentration similarity: 10%

        Revenue and EBITDA are most important, followed by market size, then customer concentration.

        You should:
        1. Compute similarity for each numeric field on a scale from 0 (very different) to 1 (very similar).
        2. Multiply each similarity by its weight.
        3. Sum the results to get a total match score.
        4. Return the top 5 companies with the highest total score.
        5. The explanation for each company should briefly describe why it was selected based on the user's criteria.

        Respond ONLY in valid JSON with this format:
        [
        {{"company": "Company Name", "score": 0.87, "reason": "Short explanation"}},
        ...
        ]
    
        Companies List: {json.dumps(companies)}
    """


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User requirements: {text}"},
    ]

    response = model.invoke(messages)
    return json.loads(response.content)
