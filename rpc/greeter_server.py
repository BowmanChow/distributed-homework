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
"""The Python implementation of the GRPC locker.Greeter server."""

from concurrent import futures
import logging

import grpc
import locker_pb2
import locker_pb2_grpc
import threading


class UpdatableBlockingQueue(object):

    def __init__(self):
        self.queue = {}
        self.cv = threading.Condition()

    def put(self, key, value):
        with self.cv:
            self.queue[key] = value
            self.cv.notify()

    def pop(self):
        with self.cv:
            while not self.queue:
                self.cv.wait()
            return self.queue.popitem()


class Locker(locker_pb2_grpc.LockerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()
        self.lock_token = -1
        self.acquire_queue = []

    def set_lock(self, token):
        self.lock.acquire()
        self.lock_token = token
        self.lock.release()
        message = f"{hex(token)} acquired lock!"
        return message


    def Lock(self, request, context):
        if request.is_acquire:
            logging.info(f"{hex(request.token)} is trying to acquire lock")
            if request.token == self.lock_token:
                message = f"lock has already been acquired by {hex(request.token)}"
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=False,
                    message=message,
                )
            elif self.lock_token == -1:
                message = self.set_lock(request.token)
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=True,
                    message=message,
                )
            else:
                self.lock.acquire()
                if request.token not in self.acquire_queue:
                    self.acquire_queue.append(request.token)
                self.lock.release()
                message = f"{hex(request.token)} waiting to acquire lock!"
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=True,
                    message=message,
                )
        else:
            logging.info(f"{hex(request.token)} is trying to release lock")
            if request.token == self.lock_token:
                self.lock.acquire()
                self.lock_token = -1
                self.lock.release()
                message = f"{hex(request.token)} released lock!"
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=True,
                    message=message,
                )
                if self.acquire_queue:
                    message = self.set_lock(self.acquire_queue[0])
                    self.acquire_queue.pop(0)
                    logging.info(message)
            elif self.lock_token == -1:
                message = f"lock is not being acquired"
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=False,
                    message=message,
                )
            else:
                message = f"lock is being acquired by others"
                logging.info(message)
                reply = locker_pb2.LockReply(
                    is_success=False,
                    message=message,
                )
        print(f"{self.acquire_queue = }")
        return reply


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    locker_pb2_grpc.add_LockerServicer_to_server(Locker(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, format='[%(levelname)s][%(asctime)s] : %(message)s', datefmt='%H:%M:%S')
    serve()
