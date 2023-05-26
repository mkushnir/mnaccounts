"""Base Resource."""
import json
from functools import wraps
from datetime import datetime

from sqlalchemy import select, text, desc, join
from sqlalchemy.exc import SQLAlchemyError

import flask
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from flask_login import login_required, current_user

from ..model import to_dict, model_arguments, list_arguments_model_mixup, filters_from_args, model_fkeys, Base
from ..model.dbaudit import DbAudit

from ..policy import policy_action
from ..utils import MyJSONEncoder

from .. import db

class SimpleResourceType(type):
    def __init__(cls, name, bases, d):
        super().__init__(name, bases, d)

        cls._list_parser = RequestParser()

        cls._list_parser.add_argument('limit', type=int, location='args')
        cls._list_parser.add_argument('offset', type=int, location='args')
        cls._list_parser.add_argument('hint', type=str, location='args')
        cls._list_parser.add_argument('hintfld', type=str, location='args')
        cls._list_parser.add_argument('hintpfx', type=str, location='args')
        cls._list_parser.add_argument('sort', type=str, location='args')

        # dx?
        cls._list_parser.add_argument('searchOperation', type=str, location='args')
        cls._list_parser.add_argument('searchValue', type=str, location='args')
        cls._list_parser.add_argument('searchExpr', type=str, location='args')
        cls._list_parser.add_argument('userData', type=str, location='args')

        # odata?
        cls._list_parser.add_argument('$top', type=str, location='args')
        cls._list_parser.add_argument('$inlinecount', type=str, location='args')

        if '_model' in d and d['_model'] is not None:
            cls._model = d['_model']
            cls._model_parser = RequestParser()
            model_arguments(cls._model_parser, cls._model)
            list_arguments_model_mixup(cls._list_parser, cls._model)


def mnerror(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            raise
            abort(400, msg=str(e))

    return wrapper


def mnaccess_policy(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if not hasattr(current_user, 'get_policy'):
            res = {
                'msg': 'mnPolicyAccess',
                'args': ['get_policy'],
            }
            return res, 403

        policy = current_user.get_policy()

        if policy:
            idx, tag, action = policy_action(
                flask.session,
                current_user,
                flask.request,
                policy,
                (
                    'api-swaccounts',
                    'api-mnaccounts',
                ))

            if action == 'reject':
                res = {
                    'msg': 'mnPolicyAccess',
                    'args': [current_user.login, idx, tag],
                }
                return res, 403

            elif action == 'null':
                res = {
                    'data': None,
                }
                return res, 200

            elif action == 'accept':
                return f(*args, **kwargs)

            else:
                res = {
                    'msg': 'mnPolicyAccess',
                    'args': [current_user.login, idx, tag],
                }
                return res, 403
        else:
            res = {
                'msg': 'mnPolicyAccess',
                'args': [current_user.login, None, None],
            }
            return res, 403

    return wrapper


class SimpleResource(Resource, metaclass=SimpleResourceType):
    _model = None

    method_decorators = {
        'get': [mnerror, mnaccess_policy, login_required],
        'post': [mnerror, mnaccess_policy, login_required],
        'put': [mnerror, mnaccess_policy, login_required],
        'delete': [mnerror, mnaccess_policy, login_required],
    }

    @classmethod
    def _filters_from_args(cls, args):
        tables, filters = filters_from_args(args, cls._model)
        return tables, filters

    @staticmethod
    def _parse_sort(args):
        if 'sort' in args and args['sort'] is not None:
            sort_pieces = args['sort'].split(':')
            if len(sort_pieces) == 0:
                sortdir = 'A'
                sortfield = 'id'

            elif len(sort_pieces) == 1:
                sortdir = sort_pieces[0]
                sortfield = 'id'

            elif len(sort_pieces) == 2:
                sortdir = sort_pieces[0]
                sortfield = sort_pieces[1]
            else:
                sortdir = None
                sortfield = None
        else:
            sortdir = None
            sortfield = None

        if sortdir not in ('A', 'D'):
            sortdir = None

        return sortdir, sortfield

    def get(self, id=None):
        #time.sleep(float(random.randrange(2000)) / 1000.0);

        args = self._list_parser.parse_args(flask.request)

        with db.session() as session:
            sortdir, sortfield = self._parse_sort(args)

            if sortdir and sortfield:
                sortattr = getattr(self._model, sortfield)
                if sortdir == 'D':
                    sortattr = desc(sortattr)
            else:
                sortattr = None

            if args['hint'] is not None:
                h = args['hint']
                pfx = args.get('hintpfx')
                fieldattr = getattr(self._model, h)

                if pfx:
                    if sortattr:
                        query = select(fieldattr).filter(
                            fieldsattr.like('{}%'.format(pfx))).distinct().order_by(
                                sortattr) #.limit(20)

                    else:
                        query = select(fieldattr).filter(fieldsattr.like('{}%'.format(pfx))).distinct() #.limit(20)
                else:
                    if sortattr is not None:
                        query = select(fieldattr).distinct().order_by(sortattr) #.limit(20)
                    else:
                        query = select(fieldattr).distinct() #.limit(20)

                result = session.execute(query)
                data = [getattr(i, h) for i in result]

            else:
                query = select(self._model)

                if id is None:
                    tables, filters = self._filters_from_args(args)

                    if filters:
                        query = query.filter(*filters)

                    if sortattr is not None:
                        query = query.order_by(sortattr)

                    if args['limit']:
                        query = query.limit(args['limit'])

                    if args['offset']:
                        query = query.offset(args['offset'])

                    result = session.execute(query)
                    data = [to_dict(i) for i in result]

                else:
                    query = query.filter(self._model.id == id)
                    e = session.execute(query).scalar()
                    data = to_dict(e)

        return {
            'data': data
        }

    def _prepare_args(self, req, args):
        return args

    def _post_commit(self, req, args, o):
        pass

    def post(self):
        args = self._model_parser.parse_args(flask.request)

        args = self._prepare_args(flask.request, args)

        with db.session() as session:
            o = self._model(**args)

            session.add(o)
            session.flush()

            session.refresh(o)

            data = to_dict(o)

            audit = DbAudit(
                id=None,
                dbts=datetime.utcnow(),
                dbuser=current_user.login,
                dbmethod='insert',
                dbmodel=self._model.__table__.name,
                dbdata=data,
            )
            session.add(audit)

            session.commit()

        self._post_commit(flask.request, args, o)

        return {
            'data': data
        }

    def put(self, id=None):
        args = self._model_parser.parse_args(flask.request)

        args = self._prepare_args(flask.request, args)

        with db.session() as session:
            o = session.query(self._model).filter(
                self._model.id == id).scalar()

            if o.id != args['id']:
                res = {
                    'msg': 'mnUserErrorInconststentArgs',
                    'args': [o.id, args],
                }
                return res, 400

            for k, v in args.items():
                setattr(o, k, v)

            data = to_dict(o)

            audit = DbAudit(
                id=None,
                dbts=datetime.utcnow(),
                dbuser=current_user.login,
                dbmethod='update',
                dbmodel=self._model.__table__.name,
                dbdata=data,
            )
            session.add(audit)

            session.commit()

        self._post_commit(flask.request, args, o)

        return {
            'data': data
        }

    def delete(self, id=None):
        with db.session() as session:
            ts = datetime.utcnow()
            if id is None:
                pass

                # for e in session.query(self._model):
                #     audit = DbAudit(
                #         id=None,
                #         dbts=ts,
                #         dbuser=current_user.login,
                #         dbmethod='delete',
                #         dbmodel=self._model.__table__.name,
                #         dbdata=to_dict(e),
                #     )
                #     session.add(audit)

                #     session.delete(e)
            else:
                e = session.query(self._model).filter(
                    self._model.id == id).scalar()

                audit = DbAudit(
                    id=None,
                    dbts=ts,
                    dbuser=current_user.login,
                    dbmethod='delete',
                    dbmodel=self._model.__table__.name,
                    dbdata=to_dict(e),
                )
                session.add(audit)

                session.delete(e)

                session.commit()

        return {
            'data': id
        }
