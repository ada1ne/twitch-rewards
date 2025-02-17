"""Custom enum type for sqlalchemy types"""

import sqlalchemy as sa


class IntEnum(
    sa.types.TypeDecorator
):  # pylint: disable=W,R  no time for a fancier solution
    """Implement a custom type to store enums as int"""

    impl = sa.Integer
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
