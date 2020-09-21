

class DAO(object):
    def __init__(self, db):
        self.db = db

    def commit(self):
        self.db.session.commit()

    def add(self, entity: object, commit: bool = True):
        self.db.session.add(entity)
        if commit:
            self.commit()

    def delete(self, entity: object, commit: bool = True):
        self.db.session.delete(entity)
        if commit:
            self.commit()

    def update(self, entity: object, commit: bool = True):
        self.db.session.merge(entity)
        if commit:
            self.commit()
