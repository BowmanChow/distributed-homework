# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC locker.Greeter client."""

from __future__ import print_function

import logging

import grpc
import locker_pb2
import locker_pb2_grpc
import random


def n_bits_1(n: int):
    return (1 << n) - 1


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logging.info("Connecting to server ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = locker_pb2_grpc.LockerStub(channel)
        while True:
            char = input("Please input operation : ")
            if char == 'a':
                response = stub.Lock(
                    locker_pb2.LockRequest(
                        is_acquire=True,
                        token=my_token,
                    )
                )
            elif char == 'r':
                response = stub.Lock(
                    locker_pb2.LockRequest(
                        is_acquire=False,
                        token=my_token,
                    )
                )
            logging.info(f"""operation success : {response.is_success}
message : {response.message}
""")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, format='[%(levelname)s][%(asctime)s] : %(message)s', datefmt='%H:%M:%S')
    my_token = random.getrandbits(64) & n_bits_1(64)
    logging.info(f"Client init : my token = {hex(my_token)}")
    run()
