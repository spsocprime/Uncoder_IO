from typing import Union, Optional

from app.translator.core.mapping import SourceMapping, DEFAULT_MAPPING_NAME
from app.translator.core.models.identifier import Identifier
from app.translator.core.custom_types.tokens import OperatorType


class Field:
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.__generic_names_map = {}

    def get_generic_field_name(self, source_id: str) -> Optional[str]:
        return self.__generic_names_map.get(source_id)

    def set_generic_names_map(self, source_mappings: list[SourceMapping], default_mapping: SourceMapping) -> None:
        generic_names_map = {
            source_mapping.source_id: source_mapping.fields_mapping.get_generic_field_name(self.source_name)
            for source_mapping in source_mappings
        }
        if DEFAULT_MAPPING_NAME not in generic_names_map:
            fields_mapping = default_mapping.fields_mapping
            generic_names_map[DEFAULT_MAPPING_NAME] = fields_mapping.get_generic_field_name(self.source_name)

        self.__generic_names_map = generic_names_map


class FieldValue:
    def __init__(self, source_name: str, operator: Identifier, value: Union[int, str, list, tuple]):
        self.field = Field(source_name=source_name)
        self.operator = operator
        self.values = []
        self.__add_value(value)

    @property
    def value(self):
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    def __add_value(self, value: Optional[Union[int, str, list, tuple]]):
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str) and value.isnumeric():
            self.values.append(int(value))
        elif value is not None and isinstance(value, (int, str)):
            self.values.append(value)

    def __add__(self, other):
        self.values.append(other)

    def __repr__(self):
        return f"{self.field.source_name} {self.operator.token_type} {self.values}"


class Keyword:
    def __init__(self, value):
        self.operator: Identifier = Identifier(token_type=OperatorType.KEYWORD)
        self.name = "keyword"
        self.values: [str] = []
        self.__add_value(value=value)

    @property
    def value(self):
        if isinstance(self.values, list) and len(self.values) == 1:
            return self.values[0]
        return self.values

    def __add_value(self, value):
        if value and isinstance(value, (list, tuple)):
            self.values.extend(value)
        elif value and isinstance(value, str):
            self.values.append(value)

    def __add__(self, other):
        if other and isinstance(other, (list, tuple)):
            self.values.extend(other)
        elif other and isinstance(other, str):
            self.values.append(other)
        return self

    def __repr__(self):
        return f"{self.name} {self.operator.token_type} {self.values}"
