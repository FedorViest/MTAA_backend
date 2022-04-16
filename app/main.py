from fastapi import FastAPI, Depends

from app.routers import admin, customer, employee, users

tags_metadata = [
    {
        "name": "Admin",
        "description": "Operations that only user authorized as **admin** can use.",
        "externalDocs": {
            "description": "Most of the code has been taken from FastAPI documentation.",
            "url": "https://fastapi.tiangolo.com"
        },
    },
    {
        "name": "Customer",
        "description": "Operations that only user authorized as **customer** can use.",
        "externalDocs": {
            "description": "Most of the code has been taken from FastAPI documentation.",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Employee",
        "description": "Operations that only user authorized as **employee** can use.",
        "externalDocs": {
            "description": "Most of the code has been taken from FastAPI documentation.",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Users",
        "description": "Operations that **every** authorized user can use. The **login** logic is also here.",
        "externalDocs": {
            "description": "Most of the code has been taken from FastAPI documentation. Login has been taken from:"
                           "https://www.youtube.com/watch?v=0sOvCWFmrtA&t=25986s&ab_channel=freeCodeCamp.org",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(users.router)


@app.get("/")
def hello():
    return "Hello from Python!"
