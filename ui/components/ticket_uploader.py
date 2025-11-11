# ui/components/tickets_uploader.py
import streamlit as st
import requests
import json

def tickets_uploader_component():
    st.subheader("📤 Upload Previous Tickets")

    uploaded_files = st.file_uploader(
        "Upload ticket files (JSON, PDF, or TXT)", 
        type=["json", "pdf", "txt"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} files ready for ingestion.")
        
        if st.button("🚀 Ingest Tickets"):
            files_data = []
            for file in uploaded_files:
                if file.type == "application/json":
                    files_data.append(json.load(file))
                else:
                    files_data.append({"filename": file.name, "content": file.getvalue(), "type": file.type})
            with st.spinner("Ingesting tickets..."):
                response = requests.post(
                    "http://localhost:8000/tickets", 
                    json={"tickets": files_data}
                )
            if response.status_code == 200:
                st.success("✅ Tickets ingested successfully!")
            else:
                st.error(f"❌ Failed to ingest tickets: {response.text}")
