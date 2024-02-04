from data.group.models import GroupModel
from shared.utils.schema.base_schema import BaseSchema


class GroupSchema(BaseSchema):
    class Meta:
        model = GroupModel
        load_instance = True
        include_relationships = True
