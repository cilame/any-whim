# brainfuck

def evaluate(code:str):
    code = cleanup(list(code))
    bmap = buildbmap(code)
    cells, ptr, cellptr, ret = [0], 0, 0, []
    while ptr < len(code):
        cmd = code[ptr]
        if cmd == ">": 
            cellptr += 1
            if cellptr == len(cells): cells.append(0)
        if cmd == "<": cellptr = 0 if cellptr <= 0 else cellptr - 1
        if cmd == "+": cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if cmd == "-": cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if cmd == "[" and cells[cellptr] == 0: ptr = bmap[ptr]
        if cmd == "]" and cells[cellptr] != 0: ptr = bmap[ptr]
        if cmd == ",": cells[cellptr] = b'\xff'
        if cmd == ".": ret.append(chr(cells[cellptr]))
        ptr += 1
    return ''.join(ret)

def cleanup(code):
    return ''.join(filter(lambda x: x in '.,[]<>+-', code))

def buildbmap(code):
    _stack, bmap = [], {}
    for pos, cmd in enumerate(code):
        if cmd == "[": _stack.append(pos)
        if cmd == "]":
            start = _stack.pop()
            bmap[start] = pos
            bmap[pos] = start
    return bmap


if __name__ == '__main__':
    s = '''++++++++[>++++++++++++++++<-]>-<+.>[-<+.>]++++++++++.'''
    ret = evaluate(s)
    print(bytes(ret.encode()))
