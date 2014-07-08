from . common import Translit

tr = Translit({' ':'_',
               '«':'~-',
               '»':'-~'}, 
              apostrophe='.', stop='~')

def code(s): return tr.code(s)
def decode(s): return tr.decode(s)
