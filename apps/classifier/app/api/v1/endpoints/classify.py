from fastapi import APIRouter, UploadFile, File
import io

from app.parsers.nubank import NubankParser
from app.classifier.classificator import TransactionClassificator
from app.models.transaction import TransactionOutputSchema

parser = NubankParser()
classificator = TransactionClassificator()

router = APIRouter(prefix="/classify", tags=["classify"])


@router.post("/bank-statement", response_model=list[TransactionOutputSchema])
async def classify_bank_statement(bank_statement: UploadFile = File(...)):

    content = (await bank_statement.read()).decode("utf-8")
    file = io.StringIO(content)
    transactions = parser.parseBankStatementCSV(file)
    for t in transactions:
        t.category = classificator.classify(t.description)

    return [TransactionOutputSchema.from_transaction(t) for t in transactions]
