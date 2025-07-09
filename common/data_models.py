# from dataclasses import dataclass
from dataclasses import dataclass
from typing import List, Tuple
import Pyro5.serializers

@dataclass
class UserTaxData:
    person_id: str
    income_data: List[Tuple[float, float]]
    has_phic: bool

Pyro5.serializers.SerializerBase.register_class_to_dict(
    UserTaxData,
    lambda obj: {
        "person_id": obj.person_id,
        "income_data": obj.income_data,
        "has_phic": obj.has_phic,
    }
)

Pyro5.serializers.SerializerBase.register_dict_to_class(
    "common.data_models.UserTaxData",
    lambda clsname, d: UserTaxData(**d)
)
