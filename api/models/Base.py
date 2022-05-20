from sqlalchemy import inspect
from datetime import datetime


class Base():
    def to_dict(self):
        res = {}
        for c in inspect(self).mapper.column_attrs:
            res[c.key] = getattr(self, c.key)
        return res

    def update(self, **args):
        for k, v in args.items():
            setattr(self, k, v)
        self.updated_at = datetime.utcnow()
