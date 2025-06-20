from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/1")
async def endpoints():
    print("Hello")
    time.sleep(5)
    print("bye")

@app.get("/2")
async def endpoints():
    print("Hello")
    await asyncio.sleep(5)
    print("bye")    


@app.get("/3")
def endpoints():
    print("Hello")
    time.sleep(5)
    print("bye")