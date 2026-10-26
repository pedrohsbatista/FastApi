from fastapi import APIRouter, Depends, HTTPException
from schemas import ProductSchema
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import Product, User

products_router = APIRouter(prefix="/products", tags=["product"])

@products_router.post("/")
async def post(product_schema: ProductSchema, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")
    
    product = Product(product_schema.code, product_schema.description, product_schema.unit_price)

    session.add(product)
    session.commit()

    return { "mensagem": "Produto adicionado com sucesso" }

@products_router.put("/{id}")
async def put(id: int, product_schema: ProductSchema, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")

    product = session.query(Product).filter(Product.id == id).first()

    if not product:
         raise HTTPException(status_code=404, detail="Produto não encontrado")

    product.code = product_schema.code
    product.description = product_schema.description
    product.unit_price = product_schema.unit_price

    session.commit()

    return { "mensagem": "Produto atualizado com sucesso" }

@products_router.delete("/{id}")
async def delete(id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")

    product = session.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    session.delete(product)
    session.commit()

    return "Produto deletado com sucesso"    

@products_router.get("/list")
async def get_list(user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")

    return session.query(Product).all()

@products_router.get("/{id}")
async def get(id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")

    product = session.query(Product).filter(Product.id == id).first();

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product
