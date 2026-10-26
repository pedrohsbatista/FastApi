from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional["bool"] = True
    admin: Optional["bool"] = False

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class ProductSchema(BaseModel):
    code: str
    description: str
    unit_price: float

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):    
    items: List[OrderItemSchema]

    class Config:
       from_attributes = True

class OrderItemSchema(BaseModel):    
    product: int
    quantity: int    

    class Config:
        from_attributes = True

class OrderSchemaResponse(BaseModel):
    id: int
    status: str
    price: float       

    class Config:
        from_attributes = True