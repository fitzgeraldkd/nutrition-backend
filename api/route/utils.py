from typing import List, Tuple, Union

from flask import request
from flask_restful import Resource

from api.model import db
from api.serializer.utils import Serializer


class SerializedResource(Resource):
    model = None
    serializer = Serializer()

    def delete(self, **kwargs) -> Tuple[dict, int]:
        instance = self.model.query.filter_by(**kwargs).one_or_404()
        db.session.delete(instance)
        db.session.commit()
        return None, 204

    def get(self, **kwargs) -> Tuple[Union[dict, List[dict]], int]:
        if "id" not in kwargs:
            return self.list()

        instance = self.model.query.filter_by(**kwargs).one_or_404()
        return self.serializer.serialize(instance), 200

    def list(self) -> Tuple[List[dict], int]:
        instances = self.model.query.all()
        return self.serializer.serialize_many(instances), 200

    def patch(self, **kwargs) -> Tuple[dict, int]:
        payload = request.get_json()
        errors = self.serializer.validate(payload, patch=True)
        if errors:
            return errors, 400

        instance = self.model.query.filter_by(**kwargs).one_or_404()
        for key, value in payload.items():
            setattr(instance, key, value)

        return self.serializer.serialize(instance), 200

    def post(self) -> Tuple[dict, int]:
        payload = request.get_json()
        errors = self.serializer.validate(payload)
        if errors:
            return errors, 400

        instance = self.model(**payload)
        db.session.add(instance)
        db.session.commit()

        return self.serializer.serialize(instance), 201
