from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, Order, User
import config
from aiogram import Bot

app = FastAPI()
bot = Bot(token=config.BOT_TOKEN)
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/", response_class=HTMLResponse)
async def show_orders(request: Request):
    db = SessionLocal()
    orders = db.query(Order).all()

    result = []
    for order in orders:
        user = db.query(User).filter(User.telegram_id == order.user_id).first()
        username = user.name if user else f"@{order.user_id}"
        phone = user.phone if user and user.phone else None
        result.append({
            "id": order.id,
            "flower": order.flower,
            "quantity": order.quantity,
            "wrapping": order.wrapping,
            "total_price": order.total_price,
            "status": order.status,
            "user_display": phone or username
        })

    return templates.TemplateResponse("index.html", {"request": request, "orders": result})


@app.get("/update/{order_id}/{new_status}")
async def update_order(order_id: int, new_status: str):
    db = SessionLocal()
    order = db.query(Order).get(order_id)

    if not order:
        return {"error": "Заказ не найден"}

    old_status = order.status
    order.status = new_status
    db.commit()

    # Отправляем клиенту уведомление о смене статуса
    await bot.send_message(order.user_id, f"Статус вашего заказа #{order_id} изменился:\n"
                                         f"{old_status} → {new_status}")

    return RedirectResponse(url="/")


@app.get("/delete/{order_id}")
async def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).get(order_id)

    if not order:
        return {"error": "Заказ не найден"}

    user_id = order.user_id
    db.delete(order)
    db.commit()

    # Опционально: отправляем уведомление клиенту
    try:
        await bot.send_message(user_id, f"Ваш заказ #{order_id} был удалён.")
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    return RedirectResponse(url="/")