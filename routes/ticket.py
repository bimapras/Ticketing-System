from typing import Annotated
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from schema.ticket import CreateTicket, ReplyTicketMessage
from local_lakebase import run_query, run_write, run_transaction
# from lakebase import run_query, run_write, run_transaction

ticket = APIRouter()

@ticket.post("/create")
def create_ticket(ticket_data: Annotated[CreateTicket, Form()]):
    query = """
        INSERT INTO tickets (
            title,
            priority,
            created_by
        )
        VALUES (%s, %s, %s)
        RETURNING ticket_id
    """

    params = (
        ticket_data.title,
        ticket_data.priority,
        ticket_data.created_by
    )

    ticket_result = run_write(query, params)
    ticket_id = ticket_result["ticket_id"]
    query = """
        INSERT INTO ticket_messages (
            ticket_id,
            author,
            message_text
        )
        VALUES (%s, %s, %s)
    """
    params = (
        ticket_id,
        ticket_data.created_by,
        ticket_data.description)
    
    run_write(query, params)
    del ticket_result, ticket_id, params, query, ticket_data

    return RedirectResponse(
        url="/",
        status_code=303,
    )
    
# @ticket.post("/add_message/{ticket_id}")
# async def add_message(ticket_id: int, message_data: ReplyTicketMessage):
    if message_data.message_text:
        query = """
            INSERT INTO ticket_messages (
                ticket_id, author, message_text
            ) 
            VALUES (%s, %s, %s)
        """
        run_write(query, (ticket_id, message_data.author, message_data.message_text))
    return {"message": "Message added successfully."}

@ticket.post("/reply")
async def reply_ticket(reply_data: ReplyTicketMessage):
    # Extract status string from nested UpdateTicketStatus model or string
    status_str = reply_data.status.status if hasattr(reply_data.status, 'status') else reply_data.status

    queries = [
        (
            "UPDATE tickets SET status = %s WHERE ticket_id = %s",
            (status_str, reply_data.ticket_id)
        )
    ]

    if reply_data.message_text and reply_data.message_text.strip():
        queries.append((
            "INSERT INTO ticket_messages (ticket_id, author, message_text) VALUES (%s, %s, %s)",
            (reply_data.ticket_id, reply_data.author, reply_data.message_text.strip())
        ))

    # Single transaction: if message fails, status update is rolled back
    run_transaction(queries)
    return {"message": f"Ticket {reply_data.ticket_id} updated successfully."}
    
# @ticket.patch("/update_status/{ticket_id}")
# async def update_status(ticket_id: int, status_data: UpdateTicketStatus):
    query = """
        UPDATE tickets
        SET status = %s
        WHERE ticket_id = %s
    """
    params = (status_data.status, ticket_id)
    run_write(query, params)
    del params, query, status_data

    return {"message": f"Ticket {ticket_id} status updated successfully."}

@ticket.get("/message/{ticket_id}")
async def get_ticket_messages(ticket_id: int):
    query = """
        SELECT author, message_text, created_at FROM ticket_messages
        WHERE ticket_id = %s
    """
    return run_query(query, (ticket_id,))

@ticket.delete("/delete/{ticket_id}")
async def delete_ticket(ticket_id: int):
    query = """
        DELETE FROM tickets 
        WHERE ticket_id = %s
    """
    run_write(query, (ticket_id,))
    del query
    return {"message": f"Ticket {ticket_id} deleted successfully."}