from web_app.models import Agreements, Contacts, Contracts, Customers, FormOfOwnerships, Objects, ProjectExecutors, \
     ProjectStatuses, Projects, Users


async def get_table_by_component(component: str):
     # Здесь нужно реализовать логику сопоставления компонента и таблицы
     # Например:
     tables = {
         "agreements": Agreements,
         "contacts": Contacts,
         "contracts": Contracts,
         "customers": Customers,
         "form-of-ownership": FormOfOwnerships,
         "objects": Objects,
         "project-executors": ProjectExecutors,
         "project-statuses": ProjectStatuses,
         "project": Projects,
         "users": Users
     }
     return tables.get(component)