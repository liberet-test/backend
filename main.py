from fastapi import FastAPI
import uvicorn
from routers import services, transactions

# TODO: Refactorizaaaaar
app = FastAPI(
    swagger_ui_parameters={"deepLinking": False},
    docs_url="/api/v1/docs",
    title="Wallet API",
    description="Liberet Challenge",
    version="2.0",
    openapi_url="/api/v1/openapi.json"
    )

app.include_router(
    services.router,
    prefix="/api/v1/service",
    tags=["Service"]
)
app.include_router(
    transactions.router,
    prefix="/api/v1/supplier/{supplier_id}/transaction",
    tags=["Wallet"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)