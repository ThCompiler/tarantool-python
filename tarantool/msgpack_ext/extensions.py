"""
This module provides Tarantool `extension`_ types handlers.

.. _extension: https://www.tarantool.io/en/doc/latest/dev_guide/internals/msgpack_extensions/
"""
# encoding: utf-8
import functools
from collections import namedtuple

from decimal import Decimal
from uuid import UUID
from tarantool.types import BoxError
from tarantool.msgpack_ext.types.datetime import Datetime
from tarantool.msgpack_ext.types.interval import Interval

import tarantool.msgpack_ext.decimal as ext_decimal
import tarantool.msgpack_ext.uuid as ext_uuid
import tarantool.msgpack_ext.error as ext_error
import tarantool.msgpack_ext.datetime as ext_datetime
import tarantool.msgpack_ext.interval as ext_interval
from tarantool.utils import version_id


class Extension(namedtuple("Extension", "decode encode type")):
    """
    MessagePack extension type handlers.

    :ivar decode: Extension type decoder.
    :vartype decode: :obj:`callable`

    :ivar encode: Extension type encoder.
    :vartype encode: :obj:`callable`

    :ivar type: Python type represented by the extension.
    :vartype type: :obj:`type`
    """


TARANTOOL_DECIMAL_MAX_DIGITS = 38
TARANTOOL_DECIMAL_MAX_DIGITS_V35 = 76


@functools.lru_cache(maxsize=None)
def init_msgpack_extensions(tarantool_version=None):
    """
    Initialize MessagePack extension type handlers.

    :param tarantool_version: Tarantool version identifier.
    :type tarantool_version: :obj:`int`, optional

    :return: Mapping from Tarantool extension type id to its handlers.
    :rtype: :obj:`dict`
    """

    max_digits = TARANTOOL_DECIMAL_MAX_DIGITS
    if tarantool_version is not None and tarantool_version >= version_id(3, 5, 0):
        max_digits = TARANTOOL_DECIMAL_MAX_DIGITS_V35

    return {
        ext_decimal.EXT_ID: Extension(
            ext_decimal.decode,
            functools.partial(ext_decimal.encode, max_digits=max_digits),
            Decimal,
        ),
        ext_uuid.EXT_ID: Extension(
            ext_uuid.decode, ext_uuid.encode, UUID,
        ),
        ext_error.EXT_ID: Extension(
            ext_error.decode, ext_error.encode, BoxError,
        ),
        ext_datetime.EXT_ID: Extension(
            ext_datetime.decode, ext_datetime.encode, Datetime,
        ),
        ext_interval.EXT_ID: Extension(
            ext_interval.decode, ext_interval.encode, Interval,
        ),
    }
