from fastapi import FastAPI, Request
from redis import Redis
import random
import uvicorn



app = FastAPI()
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def otp_key(phone):
    return f"otp:{phone}"

@app.post("/otp")
async def send_otp(request : Request):
    data = await request.json()
    otp = random.randint(100000, 999999)

    r.set(otp_key(data["phone"]),otp, ex=30) # Valid only for 30sec 
    return {"otp": otp, "success": True}

@app.post("/otp/verify")
async def verify_otp(request : Request):
    data = await request.json()
    user_otp = data["otp"]
    phone = data["phone"]

    saved_otp = r.get(otp_key(phone))

    if saved_otp == None:
        return {"status":400, "message": "Invalid OTP"}
    else :
        r.delete(otp_key(phone))
        if user_otp != saved_otp:
            return {"status":400, "message": "Invalid OTP"}
        else :
            return {"status":200, "message": "OTP verified", "success": True}
        
@app.get("/otp/{phone}/ttl")
async def get_otp_ttl(phone):
    ttl = r.ttl(otp_key(phone))
    print(phone)
    return {"ttl": ttl, "success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
