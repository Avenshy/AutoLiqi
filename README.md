# AutoLiqi

利用 WebHook（5 分钟一次） & GitHub Action CronTab（4 小时一次） 检查 `code.js`、`liqi.json`和`lqc.lqbin` 的更新，如果检测到更新，则触发 GitHub Action，将 `liqi.json` 转为 `liqi.proto` 和 `liqi_pb2.py`。

Using WebHook (every 5 minutes) & GitHub Action CronTab (every 4 hours) to check for `code.js`, `liqi.json` and `lqc.lqbin` updates, and if an update is detected, trigger the GitHub Action, and convert `liqi.json` to `liqi.proto` and `liqi_pb2.py`.

## 使用方法

在[Release](https://github.com/Avenshy/AutoLiqi/releases/latest)中下载。

## Thanks
protobufjs protobufjs-cli -> [protobufjs/protobuf.js](https://github.com/protobufjs/protobuf.js)

protoc (3.20.1) -> [Protocol Buffers](https://github.com/protocolbuffers/protobuf/releases/tag/v3.20.1)

