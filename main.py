from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

SOL_RPC = os.getenv("SOL_RPC", "https://api.mainnet-beta.solana.com")

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "SOL earnings backend"
    }

@app.get("/wallet/{address}")
def get_sol_balance(address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }

    r = requests.post(SOL_RPC, json=payload, timeout=10)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Solana RPC error")

    data = r.json()

    if "result" not in data:
        raise HTTPException(status_code=400, detail="Invalid wallet")

    lamports = data["result"]["value"]
    return {
        "wallet": address,
        "balance_sol": lamports / 1e9
    }
