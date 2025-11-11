# ui/utils/api_client.py
import requests

BASE_URL = "http://localhost:8000"

def ingest_tickets(tickets):
    return requests.post(f"{BASE_URL}/tickets", json={"tickets": tickets})

def chat_with_agent(query):
    return requests.post(f"{BASE_URL}/chat", json={"query": query})
