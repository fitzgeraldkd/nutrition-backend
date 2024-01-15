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

    def _apply_filter(self, query):
        return query.filter(self.model.user == current_user)

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
        instance = db.get_or_404(self.model, id)
        self._authorize(instance)

        db.session.delete(instance)
        db.session.commit()
        return None, 204

    def get(self, **kwargs) -> Tuple[Union[dict, List[dict]], int]:
        id = kwargs.pop(self.pk_param, None)
        if id is None:
            return self.list()

        instance = db.get_or_404(self.model, id)
        self._authorize(instance)

        return self.serializer.serialize(instance), 200

    def list(self) -> Tuple[List[dict], int]:
        instances = db.session.execute(
            self._apply_filter(db.select(self.model))
        ).scalars()
        return self.serializer.serialize_many(instances), 200

    def patch(self, **kwargs) -> Tuple[dict, int]:
        id = kwargs.pop(self.pk_param)
        payload = request.get_json()
        error = self.serializer.validate(payload, HTTPMethod.PATCH)
        if error:
            return error, 400

        instance = db.get_or_404(self.model, id)
        self._authorize(instance)

        for key, value in payload.items():
            setattr(instance, key, value)
        db.session.commit()

        return self.serializer.serialize(instance), 200

    def post(self) -> Tuple[dict, int]:
        payload = request.get_json()
        error = self.serializer.validate(payload, HTTPMethod.POST)
        if error:
            return error, 400

        self._authorize_post(payload)

        instance = self.model(**payload)
        db.session.add(instance)
        db.session.commit()

        return self.serializer.serialize(instance), 201
