grpc-msg
========

Playing with grpc for messaging

::

    python3 server.py
    python3 test.py


To regen the grpc from job.proto::

    python3 -m grpc_tools.protoc -I . --python_out=gen/ --grpc_python_out=gen job.proto && sed -i -E 's/^import.*_pb2/from . \0/' ./gen/*.py
