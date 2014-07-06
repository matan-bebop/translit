# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  MIT License  # 
# Copyright (c) 2014, Andrii Sokolov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

"""
Example usage:
    print(code("Зевес тогді кружав сивуху і оселедцем заїдав;"))
    print(decode(code("Еней був парубок моторний")))
outputs
    Zeves toghdi kruzhav syvukhu i oseledcem zajidav;
    Еней був парубок моторний
"""

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
    'э':'eh'
}

class Translit(object):

    """ Class for creating fine-tuned transliterators."""

    def __init__(self, custom_table=None, apostrophe='’', stop='·'):
        """ Translit constructor.

        Keyword parameters:
        custom_table -- a dictionary to complement (and redefine) the 
            transliterator dictionary.
        apostrophe -- a symbol that apostrophe transliterates to, default is '’'
        stop -- special symbol used inside transliterated words, default is '·'
        """
        self.stop = stop

        self.tr = {
            'йе': 'j'+ stop +'e',
            'йу': 'j'+ stop +'u',
            'йа': 'j'+ stop +'a',
            'йі': 'j'+ stop +'i',
            'ї':'ji',
            'й': 'j',
            'ь': stop +'j', # A standalone ь needs to be distinguished from й
            'ў':'w',
            'ъ': apostrophe +'h',
            '’': apostrophe
        }

        self.tr.update(consonants)
        self.tr.update(softeners)
        self.tr.update(vowels)

        # Dictionary pairs: to differentiate 'ь' and 'й' after a consonant,
        self.tr.update(dict([(k +'ь', v +'j')
                             for k,v in list(consonants.items())]))
        self.tr.update(dict([(k +'й', v + stop +'j')
                             for k,v in list(consonants.items())]))
        # to differentiate 'тя' -> 'tja' from 'тьа' etc.
        self.tr.update(dict([(ck + sk, cv + sv)
                        for ck,cv in list(consonants.items())
                        for sk,sv in list(softeners.items())]))
        # to differentiate 'йа` -> 'j.a' from 'я' -> 'ja' etc.
        self.tr.update(dict([(ck +'й'+ vk, cv + stop +'j'+ vv)
                        for ck,cv in list(consonants.items())
                        for vk,vv in list(vowels.items())]))

        # Custom table is inserted into the dictionary after everething else 
        # except the builded uppercase letters table and the reciprocal 
        # dictionary
        if custom_table:
            self.tr.update(custom_table)

        # Some letters have their romanized appropriates beginning with symbols
        # that are not alphabetical and can't be capitalized. So, the first 
        # _alphabetical_ character needs to be made uppercase to capitalize 
        # a transliterated letter appropriate.
        def smart_capitalize(s):
            for i in range(0, len(s)):
                if s[i].isalpha():
                    return s[:i] + s[i:].capitalize()
            return s

        self.tr.update(dict([(k.capitalize(), smart_capitalize(v)) 
                        for k,v in list(self.tr.items())]))
 
        # Build a table for decoding transliterated text
        def reciprocal(table):
            return dict([(val, key) for key,val in list(table.items())])

        self.reciprocal_tr = reciprocal(self.tr)

    def code(self, s, table=None):
        """ The encoding function. Takes text in s, and encodes it according
        to the table. If the table is not provided, uses the table for 
        transliterating cyrillic text stored in the Translit instance. Returns
        the resulting text -- that is, romanized text if no table is
        provided.
        """
        if not table:
            table=self.tr

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

    def decode(self, s):
        """ Decodes back to cyrillic text transliterated by the same Translit 
        instance code() method. The text is passed in s. Returns the decoded 
        text in cyrillic.
        """
        return self.code(s,  self.reciprocal_tr)

tr = Translit()

def code(s):
    """ Returns s translited for common text."""
    return tr.code(s)


def decode(s):
    """ Returns s decoded from transliteration for common text."""
    return tr.decode(s)

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        t = Translit()
        print(line, '->', t.code(line), '->', t.decode(t.code(line)))
        #print(decode(code(line)), end="")
