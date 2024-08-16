from fastapi import FastAPI
from fastapi import APIRouter
from sqlalchemy import select
from typing import List
import datetime
import uvicorn
from db import *
from models import *

app = FastAPI()


'''
запуск
uvicorn main:app --reload
Или исполнить фаил main

Документация Swagger доступна по адресу http://127.0.0.1:8000/docs.

Документация ReDoc доступна по адресу http://127.0.0.1:8000/redoc.
'''

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


#User
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(firstname=user.firstname, lastname=user.lastname,
                                  email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "user_id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.user_id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "user_id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


#Prod
@app.post("/products/", response_model=Product)
async def create_prod(product: ProductIn):
    """Создание товара в БД, create"""
    query = products.insert().values(title=product.title, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "prod_id": last_record_id}


@app.get("/products/", response_model=List[Product])
async def read_prods():
    """Чтение товаров из БД, read"""
    query = products.select()
    return await database.fetch_all(query)


@app.get("/product/{prod_id}", response_model=Product)
async def read_prod(prod_id: int):
    """Чтение одного товара из БД, read"""
    query = products.select().where(products.c.user_id == prod_id)
    return await database.fetch_one(query)


@app.put("/product/{prod_id}", response_model=Product)
async def update_prod(prod_id: int, new_prod: ProductIn):
    """Обновление товара в БД, update"""
    query = products.update().where(products.c.user_id == prod_id).values(**new_prod.dict())
    await database.execute(query)
    return {**new_prod.dict(), "prod_id": prod_id}


@app.delete("/users/{user_id}")
async def delete_prod(prod_id: int):
    """Удаление товара из БД, delete"""
    query = products.delete().where(products.c.prod_id == prod_id)
    await database.execute(query)
    return {'message': 'Product deleted'}


#Order
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    """Создание заказа в БД, create"""
    query = orders.insert().values(user_id=order.user_id, prod_id=order.product_id,
                                   date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "order_id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    """Чтение заказов из БД, read"""
    query = select(orders.c.id.label('order_id'), orders.c.date.label('date'),
                   orders.c.status.label('status'),
                   users.c.id.label('user_id'), users.c.first_name.label('firstname'),
                   users.c.last_name.label('lastname'), users.c.email.label('email'),
                   products.c.id.label('prod_id'), products.c.title.label('title'),
                   products.c.description.label('description'), products.c.price.label('price')
                   ).join(products).join(users)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    """Чтение одного заказа из БД, read"""
    query = select(orders.c.id.label('order_id'), orders.c.date.label('date'),
                   orders.c.status.label('status'),
                   users.c.id.label('user_id'), users.c.first_name.label('firstname'),
                   users.c.last_name.label('lastname'), users.c.email.label('email'),
                   products.c.id.label('prod_id'), products.c.title.label('title'),
                   products.c.description.label('description'), products.c.price.label('price')
                   ).join(products).join(users)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    """Обновление заказа в БД, update"""
    query = orders.update().where(orders.c.order_id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "order_id": order_id}


@app.delete("/orders/{order_id}")
async def delete_user(order_id: int):
    """Удаление заказа из БД, delete"""
    query = orders.delete().where(orders.c.order_id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


'''
from random import randint, choice

@app.get("/fake_data/")
async def create_note():
    MIN_PRICE = 1
    MAX_PRICE = 10_000
    user_count=100
    prod_count=100
    order_count=100
    """Добавление тестовых пользователей в БД"""
    for i in range(user_count):
        query = users.insert().values(firstname=f'firstname_{i}',
                                      lastname=f'lastname_{i}',
                                      email=f'mail{i}@m.t',
                                      password=f'password{i}')
        await database.execute(query)

    """Добавление тестовых товаров в БД"""
    for i in range(prod_count):
        query = products.insert().values(title=f'title_{i}',
                                         description=f'description_{i}',
                                         price=randint(MIN_PRICE, MAX_PRICE))
        await database.execute(query)

    """Добавление тестовых заказов в БД"""
    for i in range(order_count):
        query = orders.insert().values(user_id=randint(1, user_count),
                                       prod_id=randint(1, prod_count),
                                       date=datetime.date.today(),
                                       status=choice(['размещен', 'ожидает оплаты', 'оплачен', 'отправлен',
                                                      'доставляется', 'доставлен', 'выполнен', 'отменен']))
        await database.execute(query)

    return {'message': f'{user_count} fake users, {prod_count} fake products'
                       f'and {order_count} fake orders created'}'''

#Start
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )