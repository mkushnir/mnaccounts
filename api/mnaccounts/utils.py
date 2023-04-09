from datetime import date, datetime
import json

from sqlalchemy import String, text
from sqlalchemy.sql.ddl import _CreateBase, _DropBase
from sqlalchemy.sql import table
from sqlalchemy.ext import compiler
from sqlalchemy.event import listen

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


# sqlite view
class CreateView(_CreateBase):
    __visit_name__ = "create_view"
    def __init__(
        self,
        name,
        selectable,
        if_not_exists=False,
    ):
        super().__init__(
            element=name,
            if_not_exists=if_not_exists
        )
        self.selectable = selectable

@compiler.compiles(CreateView)
def _create_view(element, compiler):
    return 'CREATE VIEW {} {} AS {}'.format(
        'IF NOT EXISTS' if element.if_not_exists else '',
        element.element,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )



class DropView(_DropBase):
    __visit_name__ = "drop_view"
    def __init__(
        self,
        name,
        if_exists=False,
    ):
        super().__init__(
            element=name,
            if_exists=if_exists
        )


@compiler.compiles(DropView)
def _drop_view(element, compiler):
    return 'DROP VIEW {} {}'.format(
        'IF EXISTS' if element.if_exists else '',
        element.element,
    )


def view(name, selectable, metadata):
    pk = [i for i in selectable.selected_columns if i.primary_key]

    t = table(name)

    t._columns._populate_separate_keys(
        c._make_proxy(t) for c in selectable.selected_columns)

    listen(
        metadata,
        'after_create',
        CreateView(name, selectable, True))

    listen(
        metadata,
        'before_drop',
        DropView(name, True))

    return t
