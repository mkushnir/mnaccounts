from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.row import Row

from sqlalchemy import Integer, String


class IntegerNotNull(Integer):
    nullable = False


class StringNotNull(String):
    nullable = False


Base = declarative_base()


def to_dict(o):
    if isinstance(o, Row):
        colnames = o._fields

        if len(colnames) == 1:
            k = colnames[0]
            v = getattr(o, k)
            if isinstance(v, Base):
                res = to_dict(v)
            else:
                res = dict()
                res[k] = v
        else:
            res = dict()
            for k in colnames:
                v = getattr(o, k)
                if isinstance(v, Base):
                    v = to_dict(v)
                res[k] = v

    elif isinstance(o, Base):
        colnames = tuple(i.name for i in o.__table__.columns)
        res = dict((i, getattr(o, i)) for i in colnames)

    else:
        raise Exception('type of {} is not supported'.format(o))

    return res


