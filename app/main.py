from fastapi import FastAPI

### Start App ###
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}