from fastapi import FastAPI,  UploadFile, File
from workflows.main import tickets_graph
import os


app = FastAPI(title="AutoDev API Service")

@app.get('/')
def root():
    return {"message": "Server is running!!!"}

@app.post("/tickets")
async def ingest_tickets(ticket: UploadFile = File(...)):
    try:
        file_name = ticket.filename
        file_type = os.path.splitext(file_name)[1].replace(".", "").lower()
        file_path = os.path.join('./api_incoming', file_name)

        # Save file in api_incoming folder
        with open(file_path, "wb") as f:
            content = await ticket.read()
            f.write(content)

        print(f"File saved at: {file_path}")    

        tickets_graph.invoke({
            'file_name': file_name, 
            'file_type': file_type,
            'file_path': file_path
        })

        print("Graph Invoked Successfully")

    except Exception as e:
        print(f"Error in ingest ticket api: {e}")

@app.get("/tickets")
def get_tickets():
    pass

@app.post('/chat')
def chat():
    pass