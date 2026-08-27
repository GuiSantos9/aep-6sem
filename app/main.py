from os import environ

from dotenv import dotenv_values
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.routers.denuncias import router as denuncias_router
from db.connection import lifespan

config = dotenv_values(".env")
app_name = environ.get("APP_NAME") or config.get("APP_NAME") or "Inóspita API"

app = FastAPI(
    title="Inóspita API",
    description=(
        "API para registrar, consultar e acompanhar denúncias de "
        "arquitetura hostil em espaços urbanos."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(NotFoundError)
async def not_found_handler(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ConflictError)
async def conflict_handler(_: Request, exc: ConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(BusinessRuleError)
async def business_rule_handler(_: Request, exc: BusinessRuleError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


@app.get("/health", tags=["Infraestrutura"])
def health_check():
    return {"status": "ok", "app": app_name}


app.include_router(denuncias_router)

