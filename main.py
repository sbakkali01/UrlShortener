from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app=FastAPI()
templates=Jinja2Templates("templates")
@app.get('/',response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(request,name="index.html")

@app.post('/submit')
def get_long_url(data=Form(...)):
    print(data)
    print()
    return data