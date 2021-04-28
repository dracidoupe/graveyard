# This module contains magic needed to handle database with old DDCZ application
# which connects using latin2 connection, but then proceeds to write cp1250
# encoded data into those fields

# ...aaaaand few other, let's call them, missteps?

import logging

from django.db import models

logger = logging.getLogger(__name__)


class MisencodedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if isinstance(value, str):
            return value.encode("latin2").decode("cp1250")
        else:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, str):
            return value.encode("cp1250").decode("latin2")
        else:
            return value


class MisencodedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if isinstance(value, str):
            return value.encode("latin2").decode("cp1250")
        else:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, str) and not prepared:
            return value.encode("cp1250").decode("latin2")
        else:
            return value


class MisencodedIntegerField(models.CharField):
    """
    This represents a field that should be integer, but somehow ended up being
    VARCHAR() on database level. For one reason or another, data integrity problems
    DO exist there.

    This field exist to represent valid fields while choking up on invalid fields,
    represent them as 0 and report a problem to the developer.

    One day, all data will be cleaned up and this field will be ALTER TABLEd
    to (SMALL)INT/IntegerField.

    One can dream!
    """

    def from_db_value(self, value, expression, connection):
        try:
            return int(value)
        except ValueError:
            logger.exception(
                f"Integer in VARCHAR is not an integer, but {type(value)}: {value}"
            )
            return 0

    def get_db_prep_value(self, value, connection, prepared=False):
        return str(value)
