from api.serializer.utils import Serializer


class UserSerializer(Serializer):
    validation_fields = {
        "email": {"type": str, "required": True},
        "password": {"type": str, "required": True},
    }
