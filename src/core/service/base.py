import os

from fastapi.templating import Jinja2Templates


class BaseService:
    def __init__(self) -> None:
        templates_directory = os.path.join(os.path.dirname(__file__), "../../templates")
        self.templates = Jinja2Templates(directory=templates_directory)
