from fastapi import FastAPI, Request
from redis import Redis
import uvicorn



app = FastAPI()
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

BANNER_KEY = "app:banner"

@app.post("/banner")
async def post_banner(request : Request):
    data = await request.json()
    if data["message"] == None:
        data["message"] = "Welcome to our app"

    r.set(BANNER_KEY, data["message"])
    return {"message": data["message"],"success": True}

@app.get("/banner")
async def get_banner():
    banner = r.get(BANNER_KEY)
    if banner == None:
        banner = "Oops! No banner found"
    return {"banner": banner, "success": True}

@app.delete("/banner")
async def delete_banner():
    r.delete(BANNER_KEY)
    return {"message": "Banner deleted", "success": True}


@app.get("/banner/exist")
async def banner_exists():
    is_exist = r.exists(BANNER_KEY)
    return {"exists": True if is_exist ==1 else False, "success": True}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

