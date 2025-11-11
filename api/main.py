from fastapi import FastAPI,  UploadFile, File


app = FastAPI(title="AutoDev API Service")

@app.get('/')
def root():
    return {"message": "Server is running!!!"}

@app.post("/tickets")
def ingest_tickets(ticket: UploadFile = File(...)):
    try:
        pass
    except Exception as e:
        print(f"Error in ingest ticket api: {e}")

@app.get("/tickets")
def get_tickets():
    pass

@app.post('/chat')
def chat():
    pass