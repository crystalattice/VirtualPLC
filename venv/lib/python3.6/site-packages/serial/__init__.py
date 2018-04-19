"""
`serial` is an object serialization/deserialization library intended to facilitate authoring of API models which are
readable and introspective, and to expedite code and data validation and testing. `serial` supports JSON, YAML, and
XML.
"""
# region Backwards Compatibility
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, \
    with_statement

from future import standard_library

standard_library.install_aliases()
from builtins import *
from future.utils import native_str
# endregion

from serial import errors, utilities, properties, meta, hooks, test, model, request
