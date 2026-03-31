"""MainApp."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """Liefert eine einfache Hello-World-Antwort."""
    return {"message": "Hello World"}
