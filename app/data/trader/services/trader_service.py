from data.trader.models import TraderModel, TraderPositionModel
from sqlalchemy.orm import joinedload
from shared import db

def get_all_traders_id():
    all_ids = db.session.query(TraderModel.id).all()
    print(all_ids)

def get_all_position_from_trader(trader_id):
    trader_with_positions = (
        db.session.query(TraderModel)
        .filter(TraderModel.id_trader == trader_id)
        .options(joinedload(TraderModel.positions))
        .first()
    )

    positions = trader_with_positions.positions

    for position in positions:
        print(
            f"ID Trader: {position.trader.id_trader}, Time: {position.time}, Type: {position.type}, Symbol: {position.symbol}, Volume: {position.volume}")

def post_new_position(trader_id, position):
    new_position = TraderPositionModel(
        id_trader=trader_id,
        time=position['time'],
        type=position['type'],
        symbol=position['symbol'],
        volume=position['volume']
    )

    db.session.add(new_position)
    db.session.commit()


def remove_position(trader_id, position):
    db.session.query(TraderPositionModel).filter(
        TraderPositionModel.id_trader == trader_id,
        TraderPositionModel.time == position.time,
        TraderPositionModel.type == position.type,
        TraderPositionModel.symbol == position.symbol
    ).delete()
