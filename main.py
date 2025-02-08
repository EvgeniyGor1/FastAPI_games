from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI(title="Games_app")


app.mount("/static", StaticFiles(directory="src/templates/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

test_bd = {5: "five", 10: "ten"}


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")
