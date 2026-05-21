from fastapi import FastAPI
from models import Product

app = FastAPI()

products = [
    Product(1, "Laptop", 999.99, "High-performance laptop", 10),
    Product(2, "Mouse", 19.99, "Wireless mouse", 5)
]



@app.get("/")
def greet():
    return "Hello, World!"

@app.get("/products")
def get_products():
    return products