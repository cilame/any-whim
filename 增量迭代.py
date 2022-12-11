import random
import time
from collections import Iterable
import queue

import vthread

# 增量迭代的线程安全方法

q = queue.Queue()
p = queue.Queue()
# 这个 queue 是为了保证所有迭代函数执行完后才可能抛出 StopIteration
# 因为函数执行时可能会产生新的增量
# 不能在函数未执行完就判断队列为空就跳出循环

@vthread.pool(10)
def some(t=None):
    p.put('V')

    print(t)
    if t <20:
        q.put(t+1)

    p.get()

def some_iters(ls):
    if isinstance(ls,(list,tuple,Iterable)):
        for i in ls:
            q.put(i)
    else:
        q.put(ls)
    while True:
        try:
            yield q.get(timeout=1)
        except:
            if p.empty():
                raise StopIteration
            else:
                time.sleep(1)

for i in some_iters(0):
    some(i)
