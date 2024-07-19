# import os
from typing import Any
# from pylatex import Document, Command, NoEscape
from jinja2 import Environment
import hotconfig
import Document

import os


class PyJ2Md:
    def __init__(self, template: str, doc: Document.Document = None, data: Any | None = None):
        self.doc = doc or Document.Document()
        self.template = template
        self.data = data
        # doc要接收传入和公开，目前对整个系统不是特别熟悉，否则会扼杀创新与发现
        self.extensions: list[hotconfig.HotConfig] = []
        self.CONFIG = {
            # 'SUPPORT_CHINESE_LIST': False,
            # 'IN_WRITING': True
        }

    # def __getattr__(self, name:str):
    #     if name.startswith('__'):
    #         return None
    #     # if name.startswith('_') and name in self.attributes:
    #     #     return self.attributes[name]
    #     else:
    #         return super().__getattribute__(name)

    # def __setattr__(self, name, value):
    #     print("__setattr__",name, value)
    #     # 检查属性是否应该是私有的且未通过 name mangling
    #     if name.startswith('__') and len(name) > 2:
    #         self.attributes.append((name[2:], value))
    #     else:
    #         super().__setattr__(name, value)

    # def add_easy_preamble(self, key: str, value: str, options: str | None = None):
    #     if options is None:
    #         self.doc.preamble.append(Command(key, value))
    #     else:
    #         self.doc.preamble.append(Command(key, value, options))

    def add_extension(self, extension: hotconfig.HotConfig):
        if not isinstance(extension, hotconfig.HotConfig):
            raise TypeError("请传入HotConfig类型的扩展")
        self.extensions.append(extension)

    # def __add_preamble(self):
    #     # print(self.attributes)
    #     for name, value in self.attributes:
    #         if not isinstance(name, str):
    #             raise TypeError("attributes的键类型必须是str")

    #         if isinstance(value, str):
    #             # print(name[2:])
    #             self.doc.preamble.append(Command(name[2:], value))
    #         else:
    #             print(value)
    #             raise TypeError("attributes的值是未知类型：%s" % type(value))

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

        # try:
        #     self.doc.generate_pdf(
        #         base_name, clean_tex=False, compiler='xelatex')
        # except Exception as e:
        #     input(e)

        # os.startfile(os.path.join(
        #     os.path.dirname(file_path), base_name + '.pdf'))

    # def generate_pdf(self, file_path):
# test #test
    # def set_config(self, config):
    #     self.CONFIG.update(config)
