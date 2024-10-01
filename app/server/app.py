from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "I am alive and OK."}


