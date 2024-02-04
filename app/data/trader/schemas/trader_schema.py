from data.trader.models import TraderModel
from shared.utils.schema.base_schema import BaseSchema


class TraderSchema(BaseSchema):
    class Meta:
        model = TraderModel
        load_instance = True


class CustomTraderSchema(TraderSchema):
    class Meta(TraderSchema.Meta):
        fields = ("id_trader", "daily_drawdown_anchor", "daily_drawdown", "trader_url", "maximum_drawdown")
