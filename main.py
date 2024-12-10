from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from routers import user_r, product_r,purchases_r, branches_r, providers_r, categories_r, brands_r
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()

# Configurar los orígenes permitidos
origins = [
    "http://localhost",  # Orígenes específicos
    "http://localhost:3000",
    "https://teamcelular.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,  # Permitir cookies o credenciales
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Headers permitidos
)

app.include_router(user_r.router, tags=["Users"], prefix="/users")
app.include_router(purchases_r.router, tags=["Purchases"], prefix="/purchases")
app.include_router(product_r.router, tags=["Products"], prefix="/products")
app.include_router(branches_r.router, tags=["Branches"], prefix="/branches")
app.include_router(providers_r.router, tags=["Providers"], prefix="/providers")
app.include_router(categories_r.router, tags=["Categories"], prefix="/categories")
app.include_router(brands_r.router, tags=["Brands"], prefix="/brands")


@app.get("/")
def read_root():
    return {"msg": "Welcome to team celular's API!"}




