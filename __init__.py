import os
from typing import Any
from pylatex import Document, Command, NoEscape
from jinja2 import Environment
import hotconfig


class PyJ2Md:
    def __init__(self, template: str, data: Any | None = None, document: Document | None = None):

        # 初始化一个字典来存储属性值
        self.attributes = []

        if document is None:
            self.doc = Document(documentclass='ctexart')
        else:
            self.doc = document

        self.template = template
        self.data = data
        # doc要接收传入和公开，目前对整个系统不是特别熟悉，否则会扼杀创新与发现
        self.extensions: list[hotconfig.HotConfig] = []
        self.CONFIG = {
            'SUPPORT_CHINESE_LIST': False,
            'IN_WRITING': True
        }

    # def __getattr__(self, name:str):
    #     if name.startswith('__'):
    #         return None
    #     # if name.startswith('_') and name in self.attributes:
    #     #     return self.attributes[name]
    #     else:
    #         return super().__getattribute__(name)

    def __setattr__(self, name, value):
        print("__setattr__",name, value)
        # 检查属性是否应该是私有的且未通过 name mangling
        if name.startswith('__'):
            self.attributes.append((name, value))
        else:
            super().__setattr__(name, value)

    # def add_easy_preamble(self, key: str, value: str, options: str | None = None):
    #     if options is None:
    #         self.doc.preamble.append(Command(key, value))
    #     else:
    #         self.doc.preamble.append(Command(key, value, options))

    def add_extension(self, extension: hotconfig.HotConfig):
        if not isinstance(extension, hotconfig.HotConfig):
            raise TypeError("请传入HotConfig类型的扩展")
        self.extensions.append(extension)

    def __add_preamble(self):
        # print(self.attributes)
        for name, value in self.attributes:
            if not isinstance(name, str):
                raise TypeError("attributes的键类型必须是str")

            if isinstance(value, str):
                # print(name[2:])
                self.doc.preamble.append(Command(name[2:], value))
            else:
                print(value)
                raise TypeError("attributes的值是未知类型：%s" % type(value))

    def render_template(self, template):
        self.__env = Environment(
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<<',
            variable_end_string='>>',
            comment_start_string='<#',
            comment_end_string='#>'
        )

        self.__add_preamble()

        for extension in self.extensions:
            self.doc, self.data, template = extension.pre_render_template(
                self.__env, self.doc, self.data, template)

        rendered = self.__env.from_string(template).render(
            data=self.data, CONFIG=self.CONFIG)
        self.doc.append(NoEscape(rendered))

    def generate_pdf(self, file_path):

        # 仅获取文件名称，不包括路径
        file_name: str = os.path.basename(os.path.abspath(file_path))

        # 找到第一个点的位置
        first_dot_index = file_name.find('.')

        # 如果文件名中有点
        if first_dot_index != -1:
            # 分割为base_name和extension
            base_name = file_name[:first_dot_index]
            extension = file_name[first_dot_index:]
        else:
            # 如果没有点，整个文件名就是base_name，没有extension
            base_name = file_name
            extension = ''

        # base_name, extension = os.path.splitext(os.path.basename(file_path))

        print(extension)

        if extension != ".tex.j2.py":
            raise Exception("当前文件扩展名不是'.tex.j2.py'，请谨慎检查文件是否正确！")

        os.chdir(os.path.dirname(file_path))

        try:
            self.doc.generate_pdf(
                base_name, clean_tex=False, compiler='xelatex')
        except Exception as e:
            input(e)

        os.startfile(os.path.join(
            os.path.dirname(file_path), base_name + '.pdf'))

    def set_config(self, config):
        self.CONFIG.update(config)
