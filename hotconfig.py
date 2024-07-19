import abc
# from pylatex import Document
from jinja2 import Environment


class HotConfig(abc.ABC):
    def __init__(self, name: str, run: bool = True) -> None:
        super().__init__()

        self.__name = name
        self.run = run

    @property
    def NAME(self):
        """ 提供name的只读访问 """
        return self.__name

    @abc.abstractmethod
    def pre_render_template(self, env: Environment, doc: str, data: dict, template: str) -> tuple[Environment, str, dict, str]:
        if not self.run:
            return
