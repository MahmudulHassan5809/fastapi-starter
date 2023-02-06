from src.core.crud_base import CRUDBase


class AppService():
    def __init__(self, crud: CRUDBase):
        self.crud = crud
