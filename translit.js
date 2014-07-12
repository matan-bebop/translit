//////////////////////////////////////////////////////////////// MIT License //
// Copyright (c) 2014, Andrii Sokolov
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights 
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
// copies of the Software, and to permit persons to whom the Software is 
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in 
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
/////////////////////////////////////////////////////////////////////////////// 

var Translit = (function() {

var consonants = {
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
}, softeners = {
    'є':'je',
    'ю':'ju',
    'я':'ja',
    'ё':'joh'
}, vowels = {
    'а':'a',
    'е':'e',
    'и':'y',
    'і':'i',
    'о':'o',
    'у':'u',
    'ы':'yh',
    'э':'eh'
};

function merge() {

	var obj = {};

	for (var arg in arguments) {
		for (var key in arguments[arg]) {
			if (arguments[arg].hasOwnProperty(key)) {
				obj[key] = arguments[arg][key];
			}
		}
	}

	return obj;
}

function fold(res0, obj, fun) {

	var res = res0;

	for (var key in obj) {
		if (obj.hasOwnProperty(key)) {
			fun(res, key);
		}
	}

	return res;	
}

function twofold(res0, obj1, obj2, fun) {

	var res = res0;

	for (var key1 in obj1) {
		if (obj1.hasOwnProperty(key1)) {
			for (var key2 in obj2) {
				if (obj2.hasOwnProperty(key2)) {
					fun(res, key1, key2);
				}
			}
		}
	}

	return res;	
}

return {
	Transliterator : function(apostrophe, stop, custom_table) {

		function smart_capitalize(s)
		{
			for(var i = 0; i < s.length; i++) {
				if(s[i].toUpperCase() != s[i]) {
					return s.slice(0,i) + s[i].toUpperCase() + s.slice(i+1);
				}
			}
			return s;
		}

		// Defaults are suited for plain UTF-8 text
		if(!apostrophe) { apostrophe = '’';	}
		if(!stop) { stop = '·';	}

		this.tr = merge(
			{
				'йе': 'j'+ stop +'e',
				'йу': 'j'+ stop +'u',
				'йа': 'j'+ stop +'a',
				'йі': 'j'+ stop +'i',
				'ї':'ji',
				'й': 'j',
				'ь': stop +'j', // Distinguish standalone ь from й
				'ў':'w',
				'ъ': apostrophe +'h',
				'’': apostrophe 
			},

			consonants, softeners, vowels,

        	// Dictionary pairs: to differentiate 'ь' and 'й' after a consonant,
			fold({}, consonants, function(res, c) { 
				res[c +'ь'] = consonants[c] +'j';
			}),
			fold({}, consonants, function(res, c) { 
				res[c +'й'] = consonants[c] + stop +'j';
			}),
			// to differentiate 'тя' -> 'tja' from 'тьа' etc.
			twofold({}, consonants, softeners, function(res, c, s) {
				res[c + s] = consonants[c] + softeners[s];
			}),
        	// to differentiate 'йа` -> 'j.a' from 'я' -> 'ja' etc.
			twofold({}, consonants, vowels, function(res, c, v) {
				res[c +'й'+ v] = consonants[c] + stop +'j'+ vowels[v];
			})
		);

        // Custom table is inserted into the dictionary after everething else 
        // except the builded uppercase letters table and the reciprocal 
        // dictionary
		if(custom_table) {
			this.tr = merge(this.tr, custom_table);
		}

		var self = this; // A hook for what follows

		this.tr = merge(this.tr,
			fold({}, this.tr, function(res, k) { 
				res[smart_capitalize(k)] = smart_capitalize(self.tr[k]);
			})
		);

		this.reciprocal_tr = fold({}, this.tr, function(res, k) {
			res[self.tr[k]] = k;
		});
	},

	max_key_length : function(table) {
		return fold({max: 0}, table, function(res, k) {
			if(res.max < k.length) { res.max = k.length; }
		}).max;
	}
}

})();

Translit.Transliterator.prototype.code = function(str, table) {
	
	if(!table) {
		table = this.tr;
	}
	
	max_subst_len = Translit.max_key_length(table);
	str_len = str.length; // Save the real str length,
	// then add some garbage to simplify looping
	function repeat(s, n) { var r = s; while(--n) { r += s; } return r; }
	str += repeat("$", max_subst_len - 1);
	
	var res = "", i = 0;
	
	while(i < str_len) {
		for(var l = max_subst_len; l > 0; l--) {
			if(table.hasOwnProperty(str.slice(i, i+l))) {
				res += table[str.slice(i, i+l)];
				i += l;
				break;
			}
		}
		if(l == 0) {
			res += str[i++];
		}
	}

	return res;
}

Translit.Transliterator.prototype.decode = function(str) {
	return this.code(str, this.reciprocal_tr);
}
