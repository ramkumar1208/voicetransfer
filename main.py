# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

offers = {}

@app.post("/send-offer")
async def send_offer(request: Request):
    body = await request.json()
    peer_id = body["peer_id"]
    sdp = body["sdp"]
    type_ = body["type"]
    offers[peer_id] = {
        "sdp": sdp,
        "type": type_
    }
    return {"status": "offer received"}

@app.get("/get-offer/{peer_id}")
async def get_offer(peer_id: str):
    if peer_id in offers:
        return offers[peer_id]
    return JSONResponse({"error": "No offer found"}, status_code=404)

@app.post("/send-answer/{peer_id}")
async def send_answer(peer_id: str, request: Request):
    body = await request.json()
    offers[peer_id]["answer"] = {
        "sdp": body["sdp"],
        "type": body["type"]
    }
    return {"status": "answer received"}

@app.get("/get-answer/{peer_id}")
async def get_answer(peer_id: str):
    if "answer" in offers.get(peer_id, {}):
        return offers[peer_id]["answer"]
    return JSONResponse({"error": "No answer found"}, status_code=404)
