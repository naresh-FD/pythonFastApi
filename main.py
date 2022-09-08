from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """test"""
    return {"message": "Welcome to pythons World"}
