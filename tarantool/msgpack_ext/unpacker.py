"""
Tarantool `extension`_ types decoding support.

.. _extension: https://www.tarantool.io/en/doc/latest/dev_guide/internals/msgpack_extensions/
"""
from tarantool.msgpack_ext.extensions import init_msgpack_extensions


def ext_hook(code, data, unpacker=None, tarantool_version=None):
    """
    :class:`msgpack.Unpacker` decoder.

    :param code: MessagePack extension type code.
    :type code: :obj:`int`

    :param data: MessagePack extension type data.
    :type data: :obj:`bytes`

    :param unpacker: msgpack unpacker to work with common types
        (like dictionary in extended error payload)
    :type unpacker: :class:`msgpack.Unpacker`, optional

    :param tarantool_version: Tarantool version identifier.
    :type tarantool_version: :obj:`int`, optional

    :return: Decoded value.
    :rtype: :class:`decimal.Decimal` or :class:`uuid.UUID` or
         or :class:`tarantool.BoxError` or :class:`tarantool.Datetime`
         or :class:`tarantool.Interval`

    :raise: :exc:`NotImplementedError`
    """
    ext = init_msgpack_extensions(tarantool_version)

    if code in ext:
        return ext[code].decode(data, unpacker)
    raise NotImplementedError(f"Unknown msgpack extension type code {code}")
