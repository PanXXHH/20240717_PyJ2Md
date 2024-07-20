
class Document:
    def __init__(self) -> None:
        self.content = ""

    def append(self, content: str):
        self.content += content

    def export(self, path: str):
        if not path:
            raise Exception("请传入有效的 path 参数！")

        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.content)
        except Exception as e:
            print(f"无法写入文件：{path}。错误：{e}")
