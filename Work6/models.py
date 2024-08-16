import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


#User
class User(BaseModel):
    user_id: int
    firstname: str = Field(..., title='first name', max_length=40)
    lastname: str = Field(..., title='last name', max_length=80)
    email: EmailStr = Field(..., title='emai', max_length=120)


class UserIn(User):
    password: str = Field(..., title='password', min_length=6, max_length=20)



#prod
class ProductIn(BaseModel):
    title: str = Field(..., title='title', max_length=120)
    description: str = Field(default='', title='description', max_length=300)
    price: float = Field(..., title='price', gt=0, le=10_000)


class Product(ProductIn):
    prod_id: int


#Order
class Status(Enum):
    placed = 'размещен',
    unpaid = 'ожидает оплаты'
    paid = 'оплачен'
    shipped = 'отправлен'
    delivering = 'доставляется'
    delivered = 'доставлен'
    completed = 'выполнен'
    cancelled = 'отменен'


class OrderIn(BaseModel):
    user_id: int = Field(..., title='user_id')
    prod_id: int = Field(..., title='prod_id')
    date: datetime.date = Field(..., title='date')
    status: Status = Field(..., title='status')

    class Config:
        use_enum_values = True


class Order(OrderIn):
    order_id: int
    firstname: str
    lastname: str
    email: EmailStr
    title: str
    description: str
    price: float


