from fastapi import FastAPI
app=FastAPI(title="Smart inventory system")
@app.get("/")
def home():
    return {"message":"Inventory API is running"}