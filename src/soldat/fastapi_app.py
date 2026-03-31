"""MainApp."""

from fastapi import FastAPI

from soldat.router import (
    soldat_router,
)


app = FastAPI()

# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(soldat_router, prefix="/rest")



@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

