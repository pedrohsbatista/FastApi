from sqlalchemy import create_engine, Column, String, BigInteger, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Product(Base):
    __tablename__ = "product"

    id = Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    code = Column("code", String, nullable=False)
    description = Column("description", String, nullable=False)
    unit_price = Column("unitprice", Float, nullable=False)

    def __init__(self, code, description, unit_price):
        self.code = code
        self.description = description
        self.unit_price = unit_price

class Order(Base):
    __tablename__ = "order"

    # status_pedido = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # ]

    id = Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    status = Column("status", String, default="PENDENTE")
    user = Column("user", ForeignKey("user.id"), nullable=False)    
    price = Column("price", Float, nullable=False)
    items = relationship("OrderItem", cascade="all, delete-orphan")

    def __init__(self, user, items, status="PENDENTE"):
        self.user = user
        self.items = items
        self.status = status
        self.sum_price()

    def sum_price(self):
        self.price = sum(item.unit_price * item.quantity for item in self.items)

class OrderItem(Base):
    __tablename__ = "orderitem"

    id = Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    order = Column("order", ForeignKey("order.id"), nullable=False)
    product = Column("product", ForeignKey("product.id"), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    unit_price = Column("unitprice", Float, nullable=False)
    total_price = Column("totalprice", Float, nullable=False)

    def __init__(self, product, quantity, unit_price):
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = unit_price * quantity

#Comando para criação da estrutura do banco de dados
#alembic revision --autogenerate -m "Start"
#alembic upgrade head