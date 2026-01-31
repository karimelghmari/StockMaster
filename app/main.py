# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routes import products, transactions,auth
from .database import Base,engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory System", version="1.0")

# Inclut les routes
app.include_router(products.router)
app.include_router(transactions.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return RedirectResponse(url="/static/login.html")



@app.get("/login")
async def read_login():
    return FileResponse('app/static/login.html')

@app.get("/register")
async def read_register():
    return FileResponse('app/static/register.html')

@app.get("/dashboard")
async def read_dashboard():
    from fastapi.responses import FileResponse
    return FileResponse('app/static/dashboard.html')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
    