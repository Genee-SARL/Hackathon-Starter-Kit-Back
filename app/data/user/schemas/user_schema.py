from data.user.models import UserModel
from shared.utils.schema.base_schema import BaseSchema


class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = False
        include_relationships = True


class CustomUserSchema(UserSchema):
    class Meta(UserSchema.Meta):
        fields = ("id_user", "username", "server", "multiplier", "batch_size_min", "batch_size_max", "initial_balance", "actual_balance", "daily_balance")
