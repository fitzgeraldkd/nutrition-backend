class Serializer:
    def serialize(self, _instance):
        return {}

    def serialize_many(self, instances):
        return [self.serialize(instance) for instance in instances]

    def validate(self):
        return {}
