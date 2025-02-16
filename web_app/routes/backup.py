from fastapi import APIRouter, Depends, Response, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import schedule
import time
import json

import pandas as pd
from io import BytesIO
from web_app.database import get_db
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.routes.agreements import get_agreements
from web_app.routes.contacts import get_contacts
from web_app.routes.contracts import get_contracts
from web_app.routes.form_of_ownerships import get_form_of_ownerships
from web_app.routes.logs import get_logs
from web_app.routes.users import get_users
from web_app.routes.customers import get_customers
from web_app.routes.objects import get_objects


router = APIRouter()


async def generate_excel_report(db: AsyncSession):
    # Получаем данные из базы данных
    contracts_data = await get_contracts(db)
    customers_data = await get_customers(db)
    objects_data = await get_objects(db)
    agreements_data = await get_agreements(db)
    contacts_data = await get_contacts(db)
    form_of_ownerships_data = await get_form_of_ownerships(db)
    logs_data = await get_logs(db)
    # users_data = await get_users(db, user_data)

    # Преобразуем данные в DataFrame
    contracts_df = pd.DataFrame(contracts_data)
    customers_df = pd.DataFrame(customers_data)
    objects_df = pd.DataFrame(objects_data)
    agreements_df = pd.DataFrame(agreements_data)
    contacts_df = pd.DataFrame(contacts_data)
    form_of_ownerships_data_df = pd.DataFrame(form_of_ownerships_data)
    logs_df = pd.DataFrame(logs_data)
    # users_df = pd.DataFrame(users_data)

    # Создаем Excel-файл в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Добавляем каждый DataFrame на свой лист
        contracts_df.to_excel(writer, sheet_name="Contracts", index=False)
        customers_df.to_excel(writer, sheet_name="Customers", index=False)
        objects_df.to_excel(writer, sheet_name="Objects", index=False)
        agreements_df.to_excel(writer, sheet_name="Agreements", index=False)
        contacts_df.to_excel(writer, sheet_name="Contacts", index=False)
        form_of_ownerships_data_df.to_excel(
            writer, sheet_name="Form_of_ownerships", index=False
        )
        logs_df.to_excel(writer, sheet_name="Logs", index=False)
        # users_df.to_excel(writer, sheet_name='Logs', index=False)
    # Возвращаем содержимое файла
    output.seek(0)
    return output


def send_email(email: EmailStr, excel_data: bytes):
    sender_email = "your_email@example.com"  # Замените на ваш email
    sender_password = "your_password"  # Замените на ваш пароль
    receiver_email = email

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Excel Report"

    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(excel_data)
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename=report.xlsx")

    msg.attach(attachment)

    try:
        with smtplib.SMTP_SSL(
            "smtp.example.com", 465
        ) as server:  # Замените на SMTP-сервер вашего провайдера
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


def background_task(email: EmailStr, period: str, db: AsyncSession):
    def job():
        excel_data = generate_excel_report(db)
        send_email(email, excel_data)

    if period == "day":
        schedule.every().day.do(job)
    elif period == "week":
        schedule.every().week.do(job)
    elif period == "month":
        schedule.every(30).days.do(job)  # Приблизительно раз в месяц
    elif period == "year":
        schedule.every(365).days.do(job)  # Раз в год

    while True:
        schedule.run_pending()
        time.sleep(1)


@router.get("/export", response_class=Response)
async def export_to_excel(
    db: AsyncSession = Depends(get_db),
    # user_data: dict = Depends(token_verification_dependency),
):
    # Генерируем Excel-файл
    excel_file = await generate_excel_report(db)

    # Возвращаем файл как ответ
    headers = {"Content-Disposition": 'attachment; filename="report.xlsx"'}
    return Response(
        content=excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@router.post("/schedule_report")
async def schedule_report(
    email: EmailStr,
    period: str,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    allowed_periods = ["day", "week", "month", "year"]
    if period not in allowed_periods:
        raise HTTPException(
            status_code=400,
            detail="Invalid period. Allowed values: day, week, month, year",
        )

    background_tasks.add_task(background_task, email, period, db)
    return {"message": "Report scheduling started successfully"}
