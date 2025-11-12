from fastapi import FastAPI, UploadFile, File
from workflows.main import tickets_graph
import pandas as pd
import os

app = FastAPI(title="AutoDev API Service")

# Directory to store uploaded files
INCOMING_DIR = "./api_incoming"
os.makedirs(INCOMING_DIR, exist_ok=True)

# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------
@app.get('/')
def root():
    return {"message": "Server is running!!!"}

# ---------------------------------------------------------
# Ticket ingestion endpoint
# ---------------------------------------------------------
@app.post("/tickets")
async def ingest_tickets(ticket: UploadFile = File(...)):
    try:
        # Extract metadata
        file_name = ticket.filename
        file_type = os.path.splitext(file_name)[1].replace(".", "").lower()
        file_path = os.path.join(INCOMING_DIR, file_name)

        # Save file in api_incoming folder
        with open(file_path, "wb") as f:
            content = await ticket.read()
            f.write(content)
        print(f"File saved at: {file_path}")    

        # -------------------------------------------------
        # Excel processing logic (for .xlsx or .xls files)
        # -------------------------------------------------
        if file_type in ["xlsx", "xls"]:
            try:
                df = pd.read_excel(file_path)

                # Check if required columns exist
                required_columns = ["Category", "Description", "Resolution", "SOP"]
                missing = [col for col in required_columns if col not in df.columns]

                if missing:
                    print(f"Missing columns: {missing}")
                    return {
                        "status": "error",
                        "message": f"Missing columns: {', '.join(missing)}"
                    }

                # Filter the desired columns
                filtered_df = df[required_columns]

                # Save filtered file (overwrite existing)
                filtered_df.to_excel(file_path, index=False)
                print(f"✅ Filtered Excel saved: {file_path}")

            except Exception as e:
                print(f"❌ Error processing Excel: {e}")
                return {
                    "status": "error",
                    "message": f"Error processing Excel: {str(e)}"
                }

        # -------------------------------------------------
        # Invoke LangGraph after saving/processing
        # -------------------------------------------------
        tickets_graph.invoke({
            'file_name': file_name,
            'file_type': file_type,
            'file_path': file_path
        })

        print("🚀 Graph Invoked Successfully")
        return {"status": "success", "message": f"File '{file_name}' processed & graph invoked."}

    except Exception as e:
        print(f"❌ Error in ingest_tickets API: {e}")
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# Placeholder endpoints for future
# ---------------------------------------------------------
@app.get("/tickets")
def get_tickets():
    return {"message": "Get tickets endpoint (to be implemented)"}

@app.post("/chat")
def chat():
    return {"message": "Chat endpoint (to be implemented)"}
