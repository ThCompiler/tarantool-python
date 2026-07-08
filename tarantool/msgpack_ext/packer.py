"""
Tarantool `extension`_ types encoding support.

.. _extension: https://www.tarantool.io/en/doc/latest/dev_guide/internals/msgpack_extensions/
"""

from msgpack import ExtType

from tarantool.msgpack_ext.extensions import init_msgpack_extensions


def default(obj, packer=None, tarantool_version=None):
    """
    :class:`msgpack.Packer` encoder.

    :param obj: Object to encode.
    :type obj: :class:`decimal.Decimal` or :class:`uuid.UUID` or
         or :class:`tarantool.BoxError` or :class:`tarantool.Datetime`
         or :class:`tarantool.Interval`

    :param packer: msgpack packer to work with common types
        (like dictionary in extended error payload)
    :type packer: :class:`msgpack.Packer`, optional

    :param tarantool_version: Tarantool version identifier.
    :type tarantool_version: :obj:`int`, optional

    :return: Encoded value.
    :rtype: :class:`msgpack.ExtType`

    :raise: :exc:`~TypeError`
    """

    for ext_id, ext in init_msgpack_extensions(tarantool_version).items():
        if isinstance(obj, ext.type):
            return ExtType(ext_id, ext.encode(obj, packer))
    raise TypeError(f"Unknown type: {repr(obj)}")
