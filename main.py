import hashlib
from sqlite3 import connect
from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from starlette.templating import Jinja2Templates


app=FastAPI()
templates=Jinja2Templates("templates")
@app.get('/',response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(request,name="index.html")


def connect_db():
    conn=connect("db")
    cur=conn.cursor()
    return cur

def insert_into_db(params):
    cur=connect_db()
    long_url=params["long_url"]
    short_url = params["short_url"]
    cur.execute(f"""INSERT INTO my_table values("{long_url}","{short_url}")""")
    cur.connection.commit()
    cur.connection.close()


def fetch_from_db(query):
    cur=connect_db()
    data=cur.execute(query).fetchall()
    cur.connection.close()
    return data

@app.post('/submit',response_class=HTMLResponse)
def get_long_url(request:Request, data=Form()):
    res=fetch_from_db(f"""select * from my_table where long_url='{data}' """)

    if res:
        short_url=res[0][1]
    else:
        short_url = res
        short_url = short_url.split("://")[-1]
        hash = hashlib.sha1(short_url.encode("UTF-8")).hexdigest()
        short_url="http://127.0.0.1:8000"+"/redirect/"+hash[:10]
        insert_into_db({"long_url":res, "short_url":short_url})

    return templates.TemplateResponse(request=request, name="after.html", context={"short_url":short_url,"long_url":data})


@app.get('/redirect/{token}',response_class=RedirectResponse)
def redirect_to_long_url(token):
    short_url="http://127.0.0.1:8000"+"/redirect/"+token
    data=fetch_from_db(f"""select * from my_table where short_url='{short_url}' """)
    long_url=data[0][0]
    return RedirectResponse(long_url)