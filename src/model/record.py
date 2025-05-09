class Record:
    def __init__(self, title, who, result, where, when, description, category):
        self.title = title
        self.who = who
        self.result = result
        self.where = where
        self.when = when
        self.description = description
        self.category = category

class RecordError:
    def __init__(self, err):
        self.err = err

def obj_to_record(obj):
    return Record(
        title=obj.get('Titulo'),
        who=obj.get('Quem'),
        result=obj.get('Resultado'),
        where=obj.get('Onde'),
        when=obj.get('Quando'),
        description=obj.get('Descricao'),
        category=obj.get('Categoria')
    )