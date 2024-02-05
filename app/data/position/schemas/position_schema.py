from data.position.models import PositionModel
from shared.utils.schema.base_schema import BaseSchema
from marshmallow import pre_load
import datetime
import json


class PositionSchema(BaseSchema):
    class Meta:
        model = PositionModel
        load_instance = True

    @pre_load
    def process_input(self, data, **kwargs):
        if isinstance(data, str):
            data = json.loads(data.replace("'", "\""))

        data['time'] = datetime.datetime.strptime(data['time'], '%Y.%m.%d %H:%M')

        return data
