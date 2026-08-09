from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes.ticket import ticket
from local_lakebase import run_query
# from lakebase import run_query

app = FastAPI()
app.include_router(ticket, prefix="/ticket_api")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):

    tickets = run_query(
        """
        SELECT ticket_id, title, status, priority, created_by, created_at
        FROM tickets
        ORDER BY created_at DESC
        """
    )
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "tickets": tickets
        }
    )