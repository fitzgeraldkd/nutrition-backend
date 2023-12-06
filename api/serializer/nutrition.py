from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List

from flask_login import current_user

from api.serializer.utils import Serializer
from api.utils.constants import HTTPMethod

if TYPE_CHECKING:
    from api.model.nutrition import Ingredient, Instruction, Recipe


class IngredientSerializer(Serializer):
    validation_fields = {
        "name": {"type": str, "required": True},
    }

    def serialize(self, instance: Ingredient):
        return {
            "id": instance.id,
            "name": instance.name,
            "brand": instance.brand,
            "nutrition_summary": instance.nutrition_summary,
        }

    def serialize_many(self, instances) -> List[dict]:
        return [{"id": instance.id, "name": instance.name} for instance in instances]

    def validate(self, data: dict, method: str, strict=True) -> Dict[str, List[str]]:
        errors = super().validate(data, method, strict)

        if method == HTTPMethod.POST:
            data["user_id"] = current_user.id

        return errors


class InstructionSerializer(Serializer):
    validation_fields = {
        "index": {"type": int, "required": True},
        "recipe_id": {"type": int, "required": True},
        "text": {"type": str, "required": True},
    }

    def serialize(self, instance: Instruction):
        return {
            "id": instance.id,
            "index": instance.index,
            "text": instance.text,
        }


class RecipeSerializer(Serializer):
    validation_fields = {
        "name": {"type": str, "required": True},
    }

    def serialize(self, instance: Recipe):
        return {
            "id": instance.id,
            "name": instance.name,
            "instructions": InstructionSerializer().serialize_many(
                sorted(instance.instructions, key=lambda instruction: instruction.index)
            ),
        }

    def serialize_many(self, instances: List[Recipe]):
        return [{"id": instance.id, "name": instance.name} for instance in instances]

    def validate(self, data: dict, method: str, strict=True) -> Dict[str, List[str]]:
        errors = super().validate(data, method, strict)

        if method == HTTPMethod.POST:
            data["user_id"] = current_user.id

        return errors
