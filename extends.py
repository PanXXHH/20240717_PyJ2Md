import hotconfig
# from pylatex import Package, Command


class IN_WRITING(hotconfig.HotConfig):
    def __init__(self, run: bool = True) -> None:
        # print(self.__class__.__name__)
        super().__init__(name=self.__class__.__name__, run=run)

    def pre_render_template(self, env: hotconfig.Environment, doc: str, data: dict, template: str, content: str = "当前处于编辑阶段，内容还在完善中！") -> tuple[hotconfig.Environment, dict, str]:
        if not self.run:
            return env, doc, data, template

        # block_start_string = env.block_start_string
        # block_end_string = env.block_end_string
        # variable_start_string = env.variable_start_string
        # variable_end_string = env.variable_end_string
        # comment_start_string = env.comment_start_string
        # comment_end_string = env.comment_end_string

        # doc.preamble.append(Package('tcolorbox', options='most'))

        template = \
            r"""
        % 直接使用tcolorbox环境，手动设置样式
        \begin{tcolorbox}[colback=yellow!10,colframe=red!75!black,title=警告]
            """ + content + r"""
        \end{tcolorbox}
        """ + template

        return env, doc, data, template


# class SUPPORT_CHINESE_LIST(hotconfig.HotConfig):
#     def __init__(self, run: bool = True) -> None:
#         super().__init__(name=self.__class__.__name__, run=run)

#     def pre_render_template(self, env: hotconfig.Environment, data: dict, template: str, content: str = "当前处于编辑阶段，内容还在完善中！") -> tuple[hotconfig.Environment, dict, str]:
#         if not self.run:
#             return env, data, template

#         block_start_string = env.block_start_string
#         block_end_string = env.block_end_string
#         variable_start_string = env.variable_start_string
#         variable_end_string = env.variable_end_string
#         comment_start_string = env.comment_start_string
#         comment_end_string = env.comment_end_string

#         doc.preamble.append(Command('usepackage', 'zhnumber'))
#         doc.preamble.append(Command('usepackage', 'enumitem'))

#         return env, data, template
