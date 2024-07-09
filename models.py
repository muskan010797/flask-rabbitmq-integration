from datetime import datetime
from bson.objectid import ObjectId

class RandomNumber:
    def __init__(self, number, created_at=None, id=None):
        self.id = id or ObjectId()
        self.number = number
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            '_id': self.id,
            'number': self.number,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('_id'),
            number=data.get('number'),
            created_at=data.get('created_at')
        )
