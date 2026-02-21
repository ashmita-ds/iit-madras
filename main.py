from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
from fastapi.responses import Response
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Secure Upload API is running"}

# Enable CORS for POST from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # 👈 change this
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 50 * 1024  # 50KB
VALID_TOKEN = "4q1qelzqketpt33q"


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_6526: str = Header(None, alias="X-Upload-Token-6526")
):

    # 🔐 Authentication
    if x_upload_token_6526 != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 📁 File type validation
    if not file.filename.lower().endswith((".csv", ".json", ".txt")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    # 📦 File size validation
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 📊 Process CSV files only
    if file.filename.lower().endswith(".csv"):
        try:
            decoded = contents.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))
            rows = list(reader)

            row_count = len(rows)
            columns = reader.fieldnames

            total_value = 0.0
            category_counts = {}

            for row in rows:
                value = float(row["value"])
                total_value += value

                category = row["category"]
                category_counts[category] = category_counts.get(category, 0) + 1

            return {
                "email": "25ds1000059@ds.study.iitm.ac.in",
                "filename": file.filename,
                "rows": row_count,
                "columns": columns,
                "totalValue": round(total_value, 2),
                "categoryCounts": category_counts
            }

        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV format")

    # For .json or .txt just accept
    return {
        "email": "25ds1000059@ds.study.iitm.ac.in",
        "filename": file.filename,
        "message": "File accepted"
    }
@app.options("/upload")
async def options_upload():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )