from datasource.repository.repository import Repository
from datasource.service.service import Service
from datasource.service.authorization_service import AuthorizationService


class Container:
    def __init__(self):
        self.repository = Repository()
        self.service = Service(self.repository)
        self.authorization_service = AuthorizationService(self.repository)
