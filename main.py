from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import re
from io import StringIO

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode('utf-8')), delimiter=';', dtype=str)
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df['Category'] = df['Category'].str.lower().str.strip()

        food_df = df[df['Category'] == 'food']

        def clean_amount(value):
            value = value.replace(',', '.')
            value = re.sub(r'[^\d.]', '', value)
            return float(value) if value else 0.0

        food_df['Amount'] = food_df['Amount'].apply(clean_amount)
        total = round(food_df['Amount'].sum(), 2)

        return JSONResponse({
            "answer": total,
            "email": "your_email@example.com",  # <-- Change this
            "exam": "tds-2025-05-roe"
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
