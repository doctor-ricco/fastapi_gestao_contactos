from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import json

app = FastAPI()

# Modelo de dados
class Contact(BaseModel):
    id: int
    name: str
    email_addr: EmailStr
    last_changed: datetime = datetime.now()
    available: bool | None = None
#:

# Inicializar contactos a partir de JSON
with open("contacts.json", "r") as file:
    contact_data = json.load(file)
    contacts = [Contact(**contact) for contact in contact_data]

@app.get('/')
async def index():
    return {"msg": "Contact Management APP"}

@app.get('/contact/email/{email_addr}')
async def get_contact_by_email(email_addr: EmailStr):
    for contact in contacts:
        if contact.email_addr == email_addr:
            return contact
    return {"error": "Contact not found"}

@app.put('/contact/email/{email_addr}')
async def update_contact_by_email(email_addr: EmailStr, updated_contact: Contact):
    for index, contact in enumerate(contacts):
        if contact.email_addr == email_addr:
            contacts[index] = updated_contact
            contacts[index].last_changed = datetime.now()
            return {"msg": "Contact updated successfully", "contact": contacts[index]}
    return {"error": "Contact not found"}

@app.post('/contact')
async def add_new_contact(new_contact: Contact):
    for contact in contacts:
        if contact.id == new_contact.id or contact.email_addr == new_contact.email_addr:
            return {"error": "Contact with same ID or email already exists"}
    contacts.append(new_contact)
    return {"msg": "Contact added successfully", "contact": new_contact}
