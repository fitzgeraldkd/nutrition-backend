from __future__ import annotations
from typing import TYPE_CHECKING, List

from api.serializer.utils import Serializer

if TYPE_CHECKING:
    from api.model.nutrition import Instruction, Recipe


class InstructionSerializer(Serializer):
    def serialize(self, instance: Instruction):
        return {
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
