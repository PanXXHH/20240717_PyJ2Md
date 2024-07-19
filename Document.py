
class Document:
    def __init__(self) -> None:
        self.content = ""
    
    def append(self,content:str):
        self.content += content
    
    def export(self,path:str):
        ...