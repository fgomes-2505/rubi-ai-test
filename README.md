This Django + LangChain project provides:

AI-powered PDF ingestion – extract structured financial data from company PDFs.

Investment matching – suggest similar companies based on a user’s deal criteria using weighted similarity logic.

Follow these steps:
install python 3.12
git clone https://github.com/yourusername/rubi-ai.git
cd rubi-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
import the postman collection
create a .env file in the root directory and add a variable called "OPENAI_API_KEY" in the .env (follow the .env.example file)

There are two endpoints, which are:
1. http://127.0.0.1:8000/api/v1/upload-pdf/ --> upload multiple pdf's and feed the table ingestion_extracteddata
2. http://127.0.0.1:8000/api/v1/suggest-company/ --> make suggestion based on the user question and on the information stored in the database ; returns the 5 best-matching companies with reasoning

The similarity score is calculated using the following formula:
score = 0.4 * revenue_similarity +
        0.3 * ebitda_similarity +
        0.2 * market_size_similarity +
        0.1 * customer_concentration_similarity

Each similarity value is normalized between 0 (different) and 1 (identical).

This formula was created considering the following logic:

Revenue might be the main driver — you want companies of similar size.
EBITDA gives insight into profitability, slightly less critical.
Market size matters for growth potential.
Customer concentration may matter least (risk metric).

