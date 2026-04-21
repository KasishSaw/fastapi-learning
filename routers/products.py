from fastapi import APIRouter, HTTPException, status, Depends
from models.schemas import Product

router = APIRouter(
    prefix="/products",
    tags= ["Products"]
)
fake_products_db={}
@router.get("")
async def product():
    return fake_products_db

@router.post("", status_code= status.HTTP_201_CREATED)
def CreateProduct(product:Product):
    product_id = len(fake_products_db)+1
    fake_products_db[product_id] = product
    return {"id": product_id, **product.model_dump()}

@router.put("")
def updateProduct(product_id:int, product:Product):
    if product_id not in fake_products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )
    return {"id":product_id, **product.model_dump}

@router.patch("")
def partial_update_product(product_id:int, product:Product):
    if product_id not in fake_products_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product not found"
        )
    stored_product= fake_products_db[product_id].model_dump()
    update_product = product.model_dump(include_unset=True)
    stored_product.update(update_product)
    return {"id":product_id, **stored_product}