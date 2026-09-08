from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate,ProductUpdate

router = APIRouter(
    prefix = "/products",
    tags = ["products"]
)

#post method

@router.post("/")
async def create_product(
    product:ProductCreate,db:AsyncSession = Depends(get_db)
):
    new_product = Product(
        name = product.name,
        price = product.price,
        stock = product.stock,
        status = product.status,
        description = product.description,
        sku = product.sku,
        category_id = product.category_id
    )

    db.add(new_product)

    await db.commit()

    await db.refresh(new_product)

    return{
        "message":"product inserted successfully"
    }

#get method

@router.get("/")
async def get_product(db:AsyncSession = Depends(get_db)):
   
   result = await db.execute(select(Product))

   products = result.scalars().all()

   return{
    "message":"fetched successfully",
    "data":[
        {
            "id":str(product.id),
            "product_name":product.name

        }

        for product in products
    ]
   }


#    get product by id

@router.get("/{product_id}")
async def get_product_using_id(product_id:UUID,db:AsyncSession = Depends(get_db)):

    result = await db.execute(select(Product).where(Product.id == product_id))

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    return{
        "message":"product fetched successfully",
        "data":{
            "id":str(product.id),
            "name":product.name
        }


    }

    #update put method

@router.put("/{product_id}")
async def update_product(product_id:UUID,product_data:ProductUpdate,db:AsyncSession = Depends(get_db)):

    result = await db.execute(select(Product).where(Product.id == product_id))

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404,detail="product not found")

    product.name = product_data.name
    product.price = product_data.price
    product.stock = product_data.stock
    product.description = product_data.description
    product.sku = product_data.sku
    product.status = product_data.status
    product.category_id = product_data.category_id

    await db.commit()

    await db.refresh(product)


    
    
    return{
        "message":"product updated successfully",
        "data":{
            "id":str(product.id),
            "name":product.name,
            "price":product.price
        
        }


    }


@router.delete("/{product_id}")
async def delete_product(product_id:UUID,db:AsyncSession = Depends(get_db)):

    result = await db.execute(select(Product).where(Product.id == product_id))

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code = 404,detail = "product not found")
    
    await db.delete(product)

    await db.commit()
    
    return{
        "message":"successfully deleted"
        
    }

    







