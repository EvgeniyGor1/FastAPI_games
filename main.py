import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.api_v1 import user, game


app = FastAPI(title="Games_app")

app.include_router(user.router)
app.include_router(game.router)

app.mount("/static", StaticFiles(directory="src/templates/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

test_bd = {5: "five", 10: "ten"}


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
