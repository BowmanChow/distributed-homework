# RPC 锁服务

## 环境及工具

框架： gRPC

语言： python

## 运行

先安装 `python gRPC`

```bash
> python3 -m pip install grpcio
> python3 -m pip install grpcio-tools
```

然后生成 `protobuf` 文件

```bash
> python3 -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/locker.proto
```

运行服务端

```bash
> python3 ./greeter_server.py
```

运行客户端

```bash
> python3 ./greeter_client.py
```

## 基本功能展示

### 锁服务

![](images/grpc%20lock1.png)

客户端输入 `a` 表示 `acquire` ，输入 `r` 表示 `release`

可以看到客户端 `acquire` 了一次， 第二次 `acquire` 会提示已经被客户端 `acquire` ，最后成功释放

### 多客户端

![](images/grpc%20lock2.png)

每个客户端在初始化时会随机生成一个 `uint64` 的 token， 用于标识本客户端

客户端 `0x87f1b2ad973c4c01` 首先获取锁， 并成功获取

然后客户端 `0x7509ebc6adfd7626` 尝试获取锁， 此时被放入等待队列中， 等待锁被释放

然后客户端 `0x87f1b2ad973c4c01` 释放锁， 此时等待队列中的 `0x7509ebc6adfd7626` 获取锁

客户端 `0x7509ebc6adfd7626` 再次尝试获取锁， 显示已经被获取

客户端 `0x7509ebc6adfd7626` 成功释放锁


### at-most-once 语义

由于 gRPC 本身是 at-most-once 的， 因此我们这里理解为客户端发送多次  `acquire` 操作视作一次  `acquire` 操作。

这里采用一个队列实现

![](images/grpc%20lock3.png)

图中把 `acquire_queue` 即等待锁的队列打印了出来

客户端 `0x4f8230efe4d41b1a` 首先成功获取锁

然后客户端 `0xdd00ec079bda5f82` 连续 5 次获取锁， 均显示等待获取锁， 此时服务端的 `acquire_queue` 中只有一个

客户端 `0x4f8230efe4d41b1a` 成功释放锁

客户端 `0xdd00ec079bda5f82` 立即成功获取锁， 等待队列被清空