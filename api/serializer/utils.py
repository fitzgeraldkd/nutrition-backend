from collections import defaultdict
from typing import Dict, List, Optional, Tuple, TypedDict, Union

from api.utils.constants import HTTPMethod


class Validator(TypedDict):
    type: Union[type, Tuple[type, ...]]
    required: Optional[bool]


class Serializer:
    validation_fields: Dict[str, Validator] = {}

    def serialize(self, _instance) -> dict:
        return {}

    def serialize_many(self, instances) -> List[dict]:
        return [self.serialize(instance) for instance in instances]

    def validate(self, data: dict, method: str, strict=True) -> str:
        if method == HTTPMethod.POST:
            missing_keys = []
            for key, validation in self.validation_fields.items():
                if validation["required"] and key not in data:
                    missing_keys.append(key)
            if missing_keys:
                return f'These fields are required: {", ".join(missing_keys)}'

        for key, value in data.items():
            if strict and key not in self.validation_fields:
                return f"Unexpected field: {key}"
            elif not isinstance(value, self.validation_fields[key]["type"]):
                return f"Type mismatch: {key}"
            elif self.validation_fields[key]["required"] and is_empty(value):
                return f"Field cannot be empty: {key}"


def is_empty(value) -> bool:
    if value is None:
        return True
    elif isinstance(value, (bool, float, int)):
        return False
    elif isinstance(value, (dict, list, set, str, tuple)):
        return len(value) == 0
    else:
        raise Exception("Unexpected type.")
