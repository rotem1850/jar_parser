# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import construct
import enum


class ConstantTypes(enum.Enum):
    Utf8 = 1
    Integer = 3
    Float = 4
    Long = 5
    Double = 6
    ClassInfo = 7
    StringField = 8
    Fieldref = 9
    Methodref = 10
    InterfaceMethodref = 11
    NameAndType = 12
    # TODO: Add all


long_double_struct = construct.Struct(
    "high_bytes" / construct.Int32ub,
    "low_bytes" / construct.Int32ub,
)

string_struct = construct.Struct(
    "string_index" / construct.Int16ub,
)

integer_float_struct = construct.Struct(
    "bytes" / construct.Int32ub,
)

ref_struct = construct.Struct(
    "class_index" / construct.Int16ub,
    "name_and_type_index" / construct.Int16ub,
)

class_info_struct = construct.Struct(
    "name_index" / construct.Int16ub,
)

utf8_struct = construct.Struct(
    "length" / construct.Int16ub,
    "bytes" / construct.Bytes(construct.this.length),
)

name_and_type_struct = construct.Struct(
    "name_index" / construct.Int16ub,
    "descriptor_index" / construct.Int16ub,
)

tag_to_size = {ConstantTypes.Fieldref.value: ref_struct,
               ConstantTypes.Methodref.value: ref_struct,
               ConstantTypes.InterfaceMethodref.value: ref_struct,
               ConstantTypes.ClassInfo.value: class_info_struct,
               ConstantTypes.Utf8.value: utf8_struct,
               ConstantTypes.NameAndType.value: name_and_type_struct,
               ConstantTypes.Integer.value: integer_float_struct,
               ConstantTypes.Float.value: integer_float_struct,
               ConstantTypes.StringField.value: string_struct,
               ConstantTypes.Long.value: long_double_struct,
               ConstantTypes.Double.value: long_double_struct,
               }


cp_info = construct.Struct(
    "tag" / construct.Int8ub,
    # "info" / construct.Bytes(lambda this: tag_to_size[this.tag]),
    "info" / construct.Switch(construct.this.tag,
                              tag_to_size),
)

class_file = construct.Struct(
    "magic" / construct.Int32ub,
    "minor" / construct.Int16ub,
    "major" / construct.Int16ub,
    "constant_pool_count" / construct.Int16ub,
    "constant_pool" / construct.Array(construct.this.constant_pool_count - 1, cp_info),
    "access_flags" / construct.Int16ub,
    "this_class" / construct.Int16ub,
    "super_class" / construct.Int16ub,
    # TODO : No need of next fields for this exercise
)