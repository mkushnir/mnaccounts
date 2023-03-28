"""Model."""

from itertools import chain

from sqlalchemy import inspect, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.row import Row

from sqlalchemy import Integer, String

import datetime
import dateparser


class IntegerNotNull(Integer):
    nullable = False


class StringNotNull(String):
    nullable = False


Base = declarative_base()


def to_dict(o, except_=None):
    if isinstance(o, Row):
        colnames = o._fields

        if len(colnames) == 1:
            k = colnames[0]
            v = getattr(o, k)
            if isinstance(v, Base):
                res = to_dict(v)
            else:
                res = dict()
                if except_ is None or k not in except_:
                    res[k] = v
        else:
            res = dict()
            for k in colnames:
                v = getattr(o, k)
                if isinstance(v, Base):
                    v = to_dict(v)
                if except_ is None or k not in except_:
                    res[k] = v

    elif isinstance(o, Base):
        colnames = tuple(i.name for i in o.__table__.columns)
        res = dict((i, getattr(o, i)) for i in colnames if (except_ is None or i not in except_))

    else:
        raise Exception('type of {} is not supported'.format(o))

    return res


def _date(s):
    return dateparser.parse(s).date()


def _datetime(s):
    return dateparser.parse(s)


def _infer_ty(c):
    if c.type.python_type is datetime.date:
        ty = _date
    elif c.type.python_type is datetime.datetime:
        ty = _datetime
    else:
        ty = c.type.python_type
    return ty

def model_fkeys(model):
    cols = []

    inspection = inspect(model)

    if hasattr(inspection, 'mapper'):
        columns = inspection.mapper.columns

    elif hasattr(inspection, 'columns'):
        columns = inspection.columns

    else:
        columns = []

    for i in columns:
        if i.foreign_keys:
            fkeys = []
            for j in i.foreign_keys:
                fkeys.append((j.parent, j.column))
            cols.append((i, fkeys))
    return cols

def model_arguments(parser, model, only_fields=None):
    inspection = inspect(model)

    for c in inspection.mapper.columns:
        if (only_fields is None) or (c.name in only_fields):
            ty = _infer_ty(c)
            if hasattr(c, 'nullable'):
                req = not c.nullable
            else:
                if hasattr(c.type, 'nullable'):
                    req = not c.type.nullable
                else:
                    req = False
            parser.add_argument(c.name, type=ty, required=req)


def list_arguments_model_mixup(parser, model, only_fields=None):
    inspection = inspect(model)

    for c in inspection.mapper.columns:
        if (only_fields is None) or (c.name in only_fields):
            ty = _infer_ty(c)
            for fk in c.foreign_keys:
                parser.add_argument(
                    fk.target_fullname,
                    type=ty,
                    required=False,
                    location='args')

def filters_from_args(args, model):
    tables = []
    filters = []
    inspection = inspect(model)
    for c in inspection.mapper.columns:
        for fk in c.foreign_keys:
            if fk.target_fullname in args:
                v = args[fk.target_fullname]
                if v is not None:
                    tables.append(fk.column.table)
                    filters.append(fk.column == v)
                    filters.append(c == fk.column.table.c.id)

    if 'hintfld' in args \
            and 'hintpfc' in args \
            and args['hintfld'] and args['hintpfx']:
        pfx = '{}%'.format(args['hintpfx'])
        filters.append(
            getattr(model, args['hintfld']).like(pfx))

    return set(tables), filters
