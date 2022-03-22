from fastapi import FastAPI, Depends

from app.routers import admin, customer, employee, users

app = FastAPI()

app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(users.router)
