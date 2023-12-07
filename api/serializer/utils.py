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

    def validate(self, data: dict, method: str, strict=True) -> Dict[str, List[str]]:
        errors = defaultdict(list)

        if method == HTTPMethod.POST:
            for key, validation in self.validation_fields.items():
                if validation["required"] and key not in data:
                    errors[key].append("This field is required.")

        for key, value in data.items():
            if strict and key not in self.validation_fields:
                errors[key].append("Unexpected key provided.")
            elif not isinstance(value, self.validation_fields[key]["type"]):
                errors[key].append("Type mismatch.")
            elif self.validation_fields[key]["required"] and is_empty(value):
                errors[key].append("This field cannot be empty.")

        return errors


def is_empty(value) -> bool:
    if value is None:
        return True
    elif isinstance(value, (bool, float, int)):
        return False
    elif isinstance(value, (dict, list, set, str, tuple)):
        return len(value) == 0
    else:
        raise Exception("Unexpected type.")
