from fastapi import FastAPI
from routers import user_r, product_r


app = FastAPI()

app.include_router(user_r.router, tags=["Users"], prefix="/users")
app.include_router(product_r.router, tags=["Products"], prefix="/products")

@app.get("/")
def read_root():
    return {"msg": "Welcome to team celular's API!"}




