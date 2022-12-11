
'''
!function(){
  var websocket = new WebSocket("ws://127.0.0.1:8887/browser");
  websocket.onopen = function(){
    var info = 'browser:start'
    console.log(info);
    websocket.send(info)
  }
  websocket.onmessage = function(e){
    console.log('websocket.onmessage', e.data)
    // 这里处理请求参数以及对应rpc函数调用，返回参数用字符串传递回 websocket
    var ret = ''
    websocket.send(ret)
  }
}()
'''





# pip install websockets flask


WSS_SERVER_PORT = 8887
INTERFACE_POST = 5000

import json
import traceback
import threading
from urllib.parse import unquote
from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['GET'])
def main():
    try:
        info = json.dumps(dict(request.args))
        async def clientRun():
            async with websockets.connect("ws://127.0.0.1:{}/getinfo".format(WSS_SERVER_PORT)) as websocket:
                await websocket.send(info)
                return await websocket.recv()
        return asyncio.run(clientRun())
    except:
        traceback.print_exc()
        return "启动接口失败."
threading.Thread(target=app.run, kwargs={'port': INTERFACE_POST}).start()


import asyncio
import websockets
tog = False
async def echo(websocket, path):
    global tog
    async for message in websocket:
        print("path:{} message:{}".format(path, message))
        if path == '/browser':
            if message == 'browser:start':
                tog = True
                while 1:
                    await websocket.send(await que.get())
                    await res.put(await websocket.recv())
        if path == '/getinfo':
            if tog:
                await que.put(message)
                return await websocket.send(await res.get())
            return await websocket.send('browser websocket not start.')
async def main():
    global que, res
    # 兼容旧版 asyncio.Queue() 不能放在非异步函数环境中执行。
    que = asyncio.Queue()
    res = asyncio.Queue()
    async with websockets.serve(echo, "localhost", WSS_SERVER_PORT):
        await asyncio.Future()
asyncio.run(main())

