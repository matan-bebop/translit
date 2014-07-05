import re

apo = '’'
stop = '~'
space = ' '

consonants = {
    'б':'b',
    'в':'v',
    'г':'gh',
    'д':'d',
    'ж':'zh',
    'з':'z',
    'к':'k',
    'л':'l',
    'м':'m',
    'н':'n',
    'п':'p',
    'р':'r',
    'с':'s',
    'т':'t',
    'ц':'c',
    'ч':'ch',
    'ш':'sh',
    'щ':'shh',
    'ф':'f',
    'х':'kh'
}

softeners = {
    'є':'je',
    'ю':'ju',
    'я':'ja',
    'ё':'joh'
}

vowels = {
    'а':'a',
    'е':'e',
    'и':'y',
    'і':'i',
    'о':'o',
    'у':'u',
    'ы':'yh',
    'э':'eh',
}

tr = {
    'йе': 'j'+ stop +'e',
    'йу': 'j'+ stop +'u',
    'йа': 'j'+ stop +'a',
    'йі': 'j'+ stop +'i',
    'ї':'ji',
    'й': 'j',
    'ь': stop +'j', # A standalone ь needs to be distinguished from й
    'ў':'w',
    'ъ': apo +'h',
    '’': apo,
    ' ': space
}

tr.update(consonants)
tr.update(dict([(k +'ь', v +'j') for k,v in list(consonants.items())]))
tr.update(dict([(k +'й', v + stop +'j') for k,v in list(consonants.items())]))

tr.update(softeners)
tr.update(dict([(ck + sk, cv + sv)
                for ck,cv in list(consonants.items())
                for sk,sv in list(softeners.items())]))

tr.update(vowels)
tr.update(dict([(ck +'й'+ vk, cv + stop +'j'+ vv)
                for ck,cv in list(consonants.items())
                for vk,vv in list(vowels.items())]))

def smart_capitalize(s):
    for i in range(0, len(s)):
        if s[i].isalpha():
            return s[:i] + s[i:].capitalize()
    return s

tr.update(dict([(k.capitalize(), smart_capitalize(v)) 
                for k,v in list(tr.items())]))

def code(s, table=tr):
    max_subst_len = max([len(key) for key in table])
    len_s = len(s) # Save the real s length
    s += "$" * (max_subst_len-1) # Add some garbage to simplify looping

    res = ""
    i=0
    while i < len_s:
        for l in reversed(range(1, max_subst_len+1)):
            if s[i:i+l] in table:
                res += table[s[i:i+l]]
                i += l
                break
        else:
            res += s[i]
            i += 1

    return res

def reciprocal(table):
    return dict([(val, key) for key,val in list(table.items())])

reciprocal_tr = reciprocal(tr)

def decode(s):
    return code(s,  reciprocal(tr))

import sys
for line in sys.stdin:
    print(line, '->', code(line), '->', decode(code(line)))
    #print(decode(code(line)), end="")
