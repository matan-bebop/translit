from . common import Translit

tr = Translit({' ':'-',
               '«':',,',
               '»':"''"}, stop='.', apostrophe="'")

def code(s): return tr.code(s)
def decode(s): return tr.decode(s)
