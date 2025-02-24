from datetime import datetime
import pandas as pd
from io import BytesIO

from sqlalchemy.ext.asyncio import AsyncSession
from web_app.routes.agreements import get_agreements
from web_app.routes.contacts import get_contacts
from web_app.routes.contracts import get_contracts
from web_app.routes.form_of_ownerships import get_form_of_ownerships
from web_app.routes.logs import get_logs
from web_app.routes.customers import get_customers
from web_app.routes.objects import get_objects
from web_app.routes.project_executors import get_project_executors
from web_app.routes.project_statuses import get_project_statuses
from web_app.routes.projects import get_projects

from web_app.utils.core import model_to_dict


async def generate_excel_report(db: AsyncSession):
    contracts_data = await get_contracts_data(db)
    customers_data = await get_customers_data(db)
    objects_data = await get_objects_data(db)
    agreements_data = await get_agreements_data(db)
    contacts_data = await get_contacts_data(db)
    form_of_ownerships_data = await get_form_of_ownerships_data(db)
    logs_data = await get_logs_data(db)
    project_exectors_data = await get_project_executors_data(db)
    project_statuses_data = await get_project_statuses_data(db)
    projects_data = await get_projects_data(db)

    # Преобразуем данные в DataFrame
    contracts_df = pd.DataFrame(contracts_data)
    customers_df = pd.DataFrame(customers_data)
    objects_df = pd.DataFrame(objects_data)
    agreements_df = pd.DataFrame(agreements_data)
    contacts_df = pd.DataFrame(contacts_data)
    form_of_ownerships_df = pd.DataFrame(form_of_ownerships_data)
    logs_df = pd.DataFrame(logs_data)
    project_exectors_df = pd.DataFrame(project_exectors_data)
    project_statuses_df = pd.DataFrame(project_statuses_data)
    projects_df = pd.DataFrame(projects_data)

    # Создаем Excel-файл в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        contracts_df.to_excel(writer, sheet_name="Договоры", index=False)
        customers_df.to_excel(writer, sheet_name="Заказчики", index=False)
        objects_df.to_excel(writer, sheet_name="Объекты", index=False)
        agreements_df.to_excel(writer, sheet_name="Соглашения", index=False)
        contacts_df.to_excel(writer, sheet_name="Контакты", index=False)
        form_of_ownerships_df.to_excel(
            writer, sheet_name="Формы собственности", index=False
        )
        logs_df.to_excel(writer, sheet_name="Логи", index=False)
        project_exectors_df.to_excel(
            writer, sheet_name="Ответственные за проект", index=False
        )
        project_statuses_df.to_excel(writer, sheet_name="Статусы проектов", index=False)
        projects_df.to_excel(writer, sheet_name="Проекты", index=False)

    # Возвращаем содержимое файла
    output.seek(0)
    return output


async def get_contracts_data(db):
    data = await get_contracts(db)
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Шифр объекта": item["code"]["code"],
            "Наименование": item["name"],
            "Заказчик": item["customer"]["name"],
            "Исполнитель": item["executor"]["username"],
            "№ Договора": item["number"],
            "Дата подписания": item["sign_date"].strftime("%d.%m.%Y"),
            "Цена": item["price"],
            "Тема": item["theme"],
            "Эволюция": item["evolution"],
            "Соглашения": "\n".join(
                f'Номер: {agreement["id"]}\n'
                f'Наименование: {agreement["name"]}\n'
                f'Номер: {agreement["number"]}\n'
                f'Цена: {agreement["price"]}\n'
                f'Срок действия: {agreement["deadline"].strftime("%d.%m.%Y")}\n'
                for agreement in item["agreements"]
            ),
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_customers_data(db):
    data = await get_customers(db)
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Наименование": item["name"],
            "Форма собственности": item["form"]["name"],
            "Адрес": item["address"],
            "ИНН": item["inn"],
            "Комментарии": item["notes"],
            "Контакты": "\n".join(
                f'Номер: {contact["id"]}\n'
                f'Имя: {contact["first_name"]} {contact["last_name"]}\n'
                f'Должность: {contact["position"]}\n'
                f'Телефон: {contact["phone"]}\n'
                f'Почта: {contact["email"]}\n'
                for contact in item["contacts"]
            ),
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_objects_data(db):
    data = await get_objects(db)
    data = [model_to_dict(obj) for obj in data]
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Шифр объекта": item["code"],
            "Комментарии": item["comment"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_agreements_data(db):
    data = await get_agreements(db)
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Наименование": item["name"],
            "Номер соглашения": item["number"],
            "Цена": item["price"],
            "Срок действия": item["deadline"].strftime("%d.%m.%Y"),
            "Комментарии": item["notes"],
            "Договор": item["contract"]["name"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_contacts_data(db):
    data = await get_contacts(db)
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Фамилия": item["first_name"],
            "Имя": item["last_name"],
            "Отчество": item["father_name"],
            "Телефон": item["phone"],
            "Почта": item["email"],
            "Должность": item["position"],
            "Заказчик": item["customer"]["name"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_form_of_ownerships_data(db):
    data = await get_form_of_ownerships(db)
    data = [model_to_dict(obj) for obj in data]
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Наименование": item["name"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_project_statuses_data(db):
    data = await get_project_statuses(db)
    data = [model_to_dict(obj) for obj in data]
    parsed_data = []
    for item in data:

        parsed_item = {
            "Номер": item["id"],
            "Наименование": item["name"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_logs_data(db):
    data = await get_logs(db)
    parsed_data = []
    for item in data:

        parsed_item = {
            "Дата/Время": item["datetime"].strftime("%d.%m.%Y %h:%m:%s"),
            "Пользователь": item["user"],
            "Действие": item["action"],
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_projects_data(db):
    data = await get_projects(db)
    parsed_data = []
    for item in data:
        parsed_item = {
            "Номер": item["id"],
            "Объект": f'{item["object"]["code"]} - {item["object"]["name"]}',
            "Договор": f'{item["contract"]["number"]} - {item["contract"]["name"]}' if item["contract"] else None,
            "Наименование проекта": item["name"],
            "Номер проекта": item["number"],
            "Основной исполнитель": item["main_executor"]["username"],
            "Срок выполнения": item["deadline"].strftime("%d.%m.%Y"),
            "Статус проекта": item["status"]["name"],
            "Комментарии": item["notes"],
            "Исполнители проекта": "\n".join(
                f'Имя: {executor["user"]["username"]}\n'
                f'Роль: {executor["user"]["role"]}\n'
                for executor in item["project_executors"]
            ),
        }
        parsed_data.append(parsed_item)

    return parsed_data


async def get_project_executors_data(db):
    data = await get_project_executors(db)
    parsed_data = []
    for item in data:
        parsed_item = {
            "Номер": item["id"],
            "Имя пользователя": item["user"]["username"],
            "Роль": item["user"]["role"],
            "ФИО": f'{item["user"]["last_name"] or ""} {item["user"]["first_name"] or ""} {item["user"]["father_name"] or ""}'.strip(),
            "Должность": item["user"]["position"],
            "Телефон": item["user"]["phone"],
            "Почта": item["user"]["email"],
            "Проект": item["project"]["name"],  # Название проекта
            "Номер проекта": item["project"]["number"],  # Номер проекта
            "Срок выполнения": item["project"]["deadline"].strftime(
                "%d.%m.%Y"
            ),  # Срок выполнения проекта
        }
        parsed_data.append(parsed_item)

    return parsed_data
