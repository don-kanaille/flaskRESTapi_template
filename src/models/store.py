from src.db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # 80 characters limit

    # List of ItemModels; many-to-1 rel. (Back reference)
    # lazy: to not create an StoreModel for each item yet
    items = db.relationship('ItemModel', lazy='dynamic')  # self.items is no list anymore but a query builder -> .all()

    def __init__(self, name):
        self.name = name

    def json(self) -> dict:
        """
        Returns the name & items as .json string.

        :return: {'name': String, 'items': String}
        """
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}  # List comprehension

    @classmethod
    def find_by_name(cls, name: str) -> object:
        """
        Find an object by its name.

        :param name: Item name to find.
        :return: object
        """
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self) -> None:
        """
        Insert new or update existing object in data base.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete object from the data base.
        """
        db.session.delete(self)
        db.session.commit()
