def caesar(t, n, keys='abcdefghijklmnopqrstuvwxyz'):
    s = list(keys)
    r = ''
    for i in t:
        if i in s:
            r += s[(s.index(i) + n)% len(keys)]
        else:
            r += i
    return r

def morse_dec(string, a='.', b='-', p=None):
    morse = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..':'D', 
             '.':'E', '..-.':'F', '--.': 'G', '....': 'H', '..': 'I',
             '.---':'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', 
             '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', 
             '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', 
             '-..-': 'X', '-.--': 'Y', '--..': 'Z', '.----': '1', 
             '..---': '2', '...--': '3', '....-': '4', '.....': '5', 
             '-....': '6', '--...': '7', '---..': '8', '----.': '9', 
             '-----': '0', '..--..': '?', '-..-.': '/', '-.--.-': '()', 
             '-....-': '-', '.-.-.-': '.' }
    _a, _b = '.', '-'
    _names = string.split() if p is None else string.split(p)
    r = []
    for ps in _names:
        ps = ps.replace(a, _a).replace(b, _b)
        ge = morse.get(ps)
        if ge:
            r.append(ge)
        else:
            r.append('[undefined:{}]'.format(ps))
    return ''.join(r)

def morse_enc(string, a='.', b='-', p=None):
    morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
             'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
             'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
             'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
             'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
             'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
             '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
             '0': '-----', '?': '..--..', '/': '-..-.', '()': '-.--.-', 
             '-': '-....-', '.': '.-.-.-'}
    _a, _b = '.', '-'
    r = []
    for i in string:
        if i.upper() in morse:
            v = morse[i.upper()].replace(_a, a).replace(_b, b)
        else:
            v = '[undefined:{}]'.format(i)
        r.append(v)
    return ' '.join(r) if p is None else p.join(r)

if __name__ == '__main__':
    s = morse_dec('.- ... -.. ..-. .- ... -..')
    print(s)

    s = morse_enc('asdfasdfnj*(&^asdnLKE')
    print(s)