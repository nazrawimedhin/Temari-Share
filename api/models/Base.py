from sqlalchemy import inspect


class Base():
    def to_dict(self):
        return {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }
