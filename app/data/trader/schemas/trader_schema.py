from app.data.trader.models import TraderModel
from shared.utils.schema.base_schema import BaseSchema

class TraderSchema(BaseSchema):
    class Meta:
        model = TraderModel
        load_instance = True