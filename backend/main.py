from fastapi import FastAPI, File, HTTPException, UploadFile
from validation import (
    CSVValidationError,
    CSVValidationErrors,
    validation_csv_portifolio,
)

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Apenas arquivos .csv são permitidos"
        )

    content = await file.read()
    text = content.decode("utf-8")

    try:
        df, warnings = validation_csv_portifolio(text)
    except CSVValidationErrors as e:
        details = [
            f"Linha {err.line}: Coluna '{err.column}': {err.message}"
            for err in e.errors
        ]
        raise HTTPException(status_code=422, detail=details)
    except CSVValidationError as e:
        details = [f"Linha {e.line}: Coluna '{e.column}': {e.message}"]
        raise HTTPException(status_code=422, detail=details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    holdings = [
        {"symbol": row["symbol"], "name": row["name"], "weight": row["weight"]}
        for _, row in df.iterrows()
    ]

    warnings_out = [
        {"line": w.line, "column": w.column, "message": w.message} for w in warnings
    ]

    return {"holdings": holdings, "warnings": warnings_out, "errors": []}
