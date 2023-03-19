from fastapi import FastAPI
app = FastAPI()

@app.get("/hola")
async def index():
    return "hola"
