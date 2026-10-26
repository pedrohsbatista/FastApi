from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import Order, User, OrderItem, Product
from schemas import OrderSchema, OrderSchemaResponse
from typing import List


orders_router = APIRouter(prefix="/orders", tags=["orders"])

@orders_router.post("/")
async def post(order_schema: OrderSchema, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    items = []

    for item in order_schema.items:
        product = session.query(Product).filter(Product.id == item.product).first();

        item = OrderItem(
            product = item.product,
            quantity = item.quantity,
            unit_price = product.unit_price
        )   
        items.append(item)

    order = Order(
        user = user.id,
        items = items
    )   

    session.add(order)
    session.commit()
    return {"mensagem": "Pedido cadastrado com sucesso"}

@orders_router.patch("/cancel/{id}")
async def cancel(id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id == id).first();

    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")    

    if user.id != order.user and not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar esse pedido")

    order.status = "CANCELADO"
    session.commit()

    return { "mensagem": f"Pedido {order.id} cancelado com sucesso"}


@orders_router.get("/list")
async def getlist(user: User = Depends(verify_token), session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso" )

    return session.query(Order).all()   

@orders_router.get("/list_byuser", response_model=List[OrderSchemaResponse])
async def getlist_byuser(user: User = Depends(verify_token), session: Session = Depends(get_session)):
    return session.query(Order).filter(Order.user == user.id).all()

@orders_router.get("/{id}", response_model=OrderSchemaResponse)
async def get(id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.user != user.id and not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar esse recurso")
        
    return order