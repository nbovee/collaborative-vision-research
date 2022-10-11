# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: colab_vision.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63olab_vision.proto\"\xb2\x01\n\nInfo_Chunk\x12\x11\n\x02id\x18\x01 \x01(\x0b\x32\x05.uuid\x12\x15\n\x05\x63hunk\x18\x02 \x01(\x0b\x32\x06.Chunk\x12\"\n\x06\x61\x63tion\x18\x03 \x03(\x0e\x32\x12.Info_Chunk.Action\x12\r\n\x05layer\x18\x04 \x01(\x05\"G\n\x06\x41\x63tion\x12\x0b\n\x07\x41\x43T_UNK\x10\x00\x12\r\n\tACT_RESET\x10\x01\x12\x0e\n\nACT_APPEND\x10\x02\x12\x11\n\rACT_INFERENCE\x10\x03\"\xb9\x01\n\rResponse_Dict\x12\x11\n\x02id\x18\x01 \x01(\x0b\x32\x05.uuid\x12\'\n\x07keypair\x18\x02 \x03(\x0b\x32\x16.Response_Dict.Keypair\x1al\n\x07Keypair\x12\x32\n\x06result\x18\x01 \x03(\x0b\x32\".Response_Dict.Keypair.ResultEntry\x1a-\n\x0bResultEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\x15\n\x04\x44ict\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\"\x16\n\x05\x43hunk\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\"\x12\n\x04uuid\x12\n\n\x02id\x18\x01 \x01(\t\" \n\x10result_Time_Dict\x12\x0c\n\x04\x64ict\x18\x01 \x01(\t\"2\n\rFile_Metadata\x12\x0c\n\x04\x61uth\x18\x01 \x01(\t\x12\x13\n\x0b\x66ile_format\x18\x02 \x01(\t\"\x1f\n\x03\x41\x63k\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\t2\xd3\x01\n\x0c\x63olab_vision\x12\x1c\n\nuploadFile\x12\x06.Chunk\x1a\x04.Ack(\x01\x12\x1e\n\x0buploadImage\x12\x06.Chunk\x1a\x05.Dict(\x01\x12\x1f\n\x0c\x64ownloadFile\x12\x05.uuid\x1a\x06.Chunk0\x01\x12.\n\x12resultTimeDownload\x12\x05.uuid\x1a\x11.result_Time_Dict\x12\x34\n\x11\x63onstantInference\x12\x0b.Info_Chunk\x1a\x0e.Response_Dict(\x01\x30\x01\x62\x06proto3')



_INFO_CHUNK = DESCRIPTOR.message_types_by_name['Info_Chunk']
_RESPONSE_DICT = DESCRIPTOR.message_types_by_name['Response_Dict']
_RESPONSE_DICT_KEYPAIR = _RESPONSE_DICT.nested_types_by_name['Keypair']
_RESPONSE_DICT_KEYPAIR_RESULTENTRY = _RESPONSE_DICT_KEYPAIR.nested_types_by_name['ResultEntry']
_DICT = DESCRIPTOR.message_types_by_name['Dict']
_CHUNK = DESCRIPTOR.message_types_by_name['Chunk']
_UUID = DESCRIPTOR.message_types_by_name['uuid']
_RESULT_TIME_DICT = DESCRIPTOR.message_types_by_name['result_Time_Dict']
_FILE_METADATA = DESCRIPTOR.message_types_by_name['File_Metadata']
_ACK = DESCRIPTOR.message_types_by_name['Ack']
_INFO_CHUNK_ACTION = _INFO_CHUNK.enum_types_by_name['Action']
Info_Chunk = _reflection.GeneratedProtocolMessageType('Info_Chunk', (_message.Message,), {
  'DESCRIPTOR' : _INFO_CHUNK,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:Info_Chunk)
  })
_sym_db.RegisterMessage(Info_Chunk)

Response_Dict = _reflection.GeneratedProtocolMessageType('Response_Dict', (_message.Message,), {

  'Keypair' : _reflection.GeneratedProtocolMessageType('Keypair', (_message.Message,), {

    'ResultEntry' : _reflection.GeneratedProtocolMessageType('ResultEntry', (_message.Message,), {
      'DESCRIPTOR' : _RESPONSE_DICT_KEYPAIR_RESULTENTRY,
      '__module__' : 'colab_vision_pb2'
      # @@protoc_insertion_point(class_scope:Response_Dict.Keypair.ResultEntry)
      })
    ,
    'DESCRIPTOR' : _RESPONSE_DICT_KEYPAIR,
    '__module__' : 'colab_vision_pb2'
    # @@protoc_insertion_point(class_scope:Response_Dict.Keypair)
    })
  ,
  'DESCRIPTOR' : _RESPONSE_DICT,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:Response_Dict)
  })
_sym_db.RegisterMessage(Response_Dict)
_sym_db.RegisterMessage(Response_Dict.Keypair)
_sym_db.RegisterMessage(Response_Dict.Keypair.ResultEntry)

Dict = _reflection.GeneratedProtocolMessageType('Dict', (_message.Message,), {
  'DESCRIPTOR' : _DICT,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:Dict)
  })
_sym_db.RegisterMessage(Dict)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), {
  'DESCRIPTOR' : _CHUNK,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:Chunk)
  })
_sym_db.RegisterMessage(Chunk)

uuid = _reflection.GeneratedProtocolMessageType('uuid', (_message.Message,), {
  'DESCRIPTOR' : _UUID,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:uuid)
  })
_sym_db.RegisterMessage(uuid)

result_Time_Dict = _reflection.GeneratedProtocolMessageType('result_Time_Dict', (_message.Message,), {
  'DESCRIPTOR' : _RESULT_TIME_DICT,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:result_Time_Dict)
  })
_sym_db.RegisterMessage(result_Time_Dict)

File_Metadata = _reflection.GeneratedProtocolMessageType('File_Metadata', (_message.Message,), {
  'DESCRIPTOR' : _FILE_METADATA,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:File_Metadata)
  })
_sym_db.RegisterMessage(File_Metadata)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'colab_vision_pb2'
  # @@protoc_insertion_point(class_scope:Ack)
  })
_sym_db.RegisterMessage(Ack)

_COLAB_VISION = DESCRIPTOR.services_by_name['colab_vision']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RESPONSE_DICT_KEYPAIR_RESULTENTRY._options = None
  _RESPONSE_DICT_KEYPAIR_RESULTENTRY._serialized_options = b'8\001'
  _INFO_CHUNK._serialized_start=23
  _INFO_CHUNK._serialized_end=201
  _INFO_CHUNK_ACTION._serialized_start=130
  _INFO_CHUNK_ACTION._serialized_end=201
  _RESPONSE_DICT._serialized_start=204
  _RESPONSE_DICT._serialized_end=389
  _RESPONSE_DICT_KEYPAIR._serialized_start=281
  _RESPONSE_DICT_KEYPAIR._serialized_end=389
  _RESPONSE_DICT_KEYPAIR_RESULTENTRY._serialized_start=344
  _RESPONSE_DICT_KEYPAIR_RESULTENTRY._serialized_end=389
  _DICT._serialized_start=391
  _DICT._serialized_end=412
  _CHUNK._serialized_start=414
  _CHUNK._serialized_end=436
  _UUID._serialized_start=438
  _UUID._serialized_end=456
  _RESULT_TIME_DICT._serialized_start=458
  _RESULT_TIME_DICT._serialized_end=490
  _FILE_METADATA._serialized_start=492
  _FILE_METADATA._serialized_end=542
  _ACK._serialized_start=544
  _ACK._serialized_end=575
  _COLAB_VISION._serialized_start=578
  _COLAB_VISION._serialized_end=789
# @@protoc_insertion_point(module_scope)
