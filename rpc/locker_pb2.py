# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: locker.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0clocker.proto\x12\x06locker\"0\n\x0bLockRequest\x12\x12\n\nis_acquire\x18\x01 \x01(\x08\x12\r\n\x05token\x18\x02 \x01(\x04\"0\n\tLockReply\x12\x12\n\nis_success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2:\n\x06Locker\x12\x30\n\x04Lock\x12\x13.locker.LockRequest\x1a\x11.locker.LockReply\"\x00\x42.\n\x17io.grpc.examples.lockerB\x0bLockerProtoP\x01\xa2\x02\x03HLWb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'locker_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027io.grpc.examples.lockerB\013LockerProtoP\001\242\002\003HLW'
  _LOCKREQUEST._serialized_start=24
  _LOCKREQUEST._serialized_end=72
  _LOCKREPLY._serialized_start=74
  _LOCKREPLY._serialized_end=122
  _LOCKER._serialized_start=124
  _LOCKER._serialized_end=182
# @@protoc_insertion_point(module_scope)