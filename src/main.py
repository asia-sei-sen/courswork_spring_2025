import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from invest_savings import investkopilka, read_transactions_from_excel

app = FastAPI()

@app.get("/investkopilka")
async def get_investkopilka(
    month: str = Query(..., regex=r"^\d{4}-\d{2}$"),
    round_limit: int = Query(10, gt=0)
):
    transactions = read_transactions_from_excel("data/operations.xlsx")
    result_json = investkopilka(month, transactions, round_limit)
    return JSONResponse(content=json.loads(result_json))
