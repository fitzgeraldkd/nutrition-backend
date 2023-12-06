from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple, Union

from flask import abort, request
from flask_login import current_user
from flask_restful import Resource

from api import db
from api.serializer.utils import Serializer
from api.utils.constants import HTTPMethod


if TYPE_CHECKING:
    from api.model.user import User


class SerializedResource(Resource):
    model = None
    serializer = Serializer()
    pk_param = "id"

    def _get_parent_owners(self, payload: dict) -> List[User]:
        return []

    def _authorize(self, instance=None):
        if instance.get_owner() != current_user:
            abort(403)

    def _authorize_post(self, payload: dict):
        """
        When creating a new object that does not directly link to a User, assert that all of the related objects are
        owned by the user making the request.
        """
        if any([owner != current_user for owner in self._get_parent_owners(payload)]):
            abort(403)

    def delete(self, **kwargs) -> Tuple[dict, int]:
        id = kwargs.pop(self.pk_param)
        instance = self.model.query.filter_by(id=id, **kwargs).one_or_404()
        self._authorize(instance)

        db.session.delete(instance)
        db.session.commit()
        return None, 204

    def get(self, **kwargs) -> Tuple[Union[dict, List[dict]], int]:
        id = kwargs.pop(self.pk_param, None)
        if id is None:
            return self.list()

        instance = self.model.query.filter_by(id=id, **kwargs).one_or_404()
        self._authorize(instance)

        return self.serializer.serialize(instance), 200

    def list(self) -> Tuple[List[dict], int]:
        instances = self.model.query.all()
        return self.serializer.serialize_many(instances), 200

    def patch(self, **kwargs) -> Tuple[dict, int]:
        id = kwargs.pop(self.pk_param)
        payload = request.get_json()
        errors = self.serializer.validate(payload, HTTPMethod.PATCH)
        if errors:
            return errors, 400

        instance = self.model.query.filter_by(id=id, **kwargs).one_or_404()
        self._authorize(instance)

        for key, value in payload.items():
            setattr(instance, key, value)

        return self.serializer.serialize(instance), 200

    def post(self) -> Tuple[dict, int]:
        payload = request.get_json()
        errors = self.serializer.validate(payload, HTTPMethod.POST)
        if errors:
            return errors, 400

        self._authorize_post(payload)

        instance = self.model(**payload)
        db.session.add(instance)
        db.session.commit()

        return self.serializer.serialize(instance), 201
