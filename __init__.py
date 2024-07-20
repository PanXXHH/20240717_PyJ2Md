from typing import Any
from jinja2 import Environment
import hotconfig
import Document


class PyJ2Md:
    def __init__(self, template: str, data: Any = None, doc: Document.Document | None = None):
        self.template = template
        self.data = data
        self.doc = doc or Document.Document()
        # doc要接收传入和公开，目前对整个系统不是特别熟悉，否则会扼杀创新与发现
        self.extensions: list[hotconfig.HotConfig] = []
        self.CONFIG = {
            # 'SUPPORT_CHINESE_LIST': False,
        }

    def add_extension(self, extension: hotconfig.HotConfig):
        if not isinstance(extension, hotconfig.HotConfig):
            raise TypeError("请传入HotConfig类型的扩展")
        self.extensions.append(extension)

    def render_template(self, template, env: Environment | None = None):
        if env is None:
            self.__env = Environment(
                block_start_string='<%',
                block_end_string='%>',
                variable_start_string='<<',
                variable_end_string='>>',
                comment_start_string='<#',
                comment_end_string='#>'
            )

        for extension in self.extensions:
            self.doc, self.data, template = extension.pre_render_template(
                self.__env, self.doc, self.data, template)

        # 使用环境来渲染模板
        rendered = self.__env.from_string(template).render(
            data=self.data, CONFIG=self.CONFIG)

        self.doc.append(rendered)

    def generate_md(self, output_path: str | None = None):

        # 如果提供了输出路径，则将渲染的内容写入文件
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(self.doc.content)
            except Exception as e:
                print(f"无法写入文件：{output_path}。错误：{e}")
