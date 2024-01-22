from app.data.trader.models import TraderPositionModel
from shared.utils.schema.base_schema import BaseSchema

class TraderPositionSchema(BaseSchema):
    class Meta:
        model = TraderPositionModel
        load_instance = True
