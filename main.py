from db_config import session, engine
from fastapi import Depends, FastAPI
from db_model import Product
import db_model
import models
from sqlalchemy.orm import Session


app = FastAPI()

db_model.Base.metadata.create_all(bind=engine)

products = [
    models.Product(id=1, name="Laptop", price=999.99, description="High-performance laptop", quantity=10),
    models.Product(id=2, name="Mouse", price=19.99, description="Wireless mouse", quantity=5)
]

def init_db():
    db= session()
    count = db.query(Product).count()
    if count ==0:
        for product in products:
            db.add(db_model.Product(**product.model_dump()))
        db.commit()

init_db()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Hello, World!"

@app.get("/products")
def get_products(db: Session= Depends(get_db)):     
    return db.query(Product).all()

@app.get("/product/{product_id}")
def get_product_by_id(product_id: int, db : Session=Depends(get_db)):  # Dependency injection to get the database session
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post("/product")
def add_products(product: models.Product, db : Session=Depends(get_db)):
    db.add(db_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.delete("/product")
def delete_product(product_id: int,db : Session=Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    return "Product not found"

@app.put("/product")
def update_product(product_id: int, updated_product: models.Product, db : Session=Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.price = updated_product.price
        db_product.description = updated_product.description
        db_product.quantity = updated_product.quantity
        db.commit()
        return "Product updated successfully"
    return "Product not found"
