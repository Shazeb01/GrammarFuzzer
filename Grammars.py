#!/usr/bin/env python3

#defining start piont
START_SYMBOL = "<start>"

#importing labraries
import random
import re
from GrammarFuzzer import GrammarFuzzer

#defining raw string in regex
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

def nonterminals(expansion):
    if isinstance(expansion, tuple):
        expansion = expansion[0]
    #searching the raw string in expansion and returning it
    return re.findall(RE_NONTERMINAL, expansion)

if __name__ == "__main__":
    assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
    assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
    assert nonterminals("1 < 3 > 2") == []
    assert nonterminals("1 <3> 2") == ["<3>"]
    assert nonterminals("1 + 2") == []
    assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]


def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)

if __name__ == "__main__":
    assert is_nonterminal("<abc>")
    assert is_nonterminal("<symbol-1>")
    assert not is_nonterminal("+")

#Creating Error class
class ExpansionError(Exception):
    pass

#defining a fuzzer
def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term




#defining grammar for fake name and number
Fake_Name = {
    "<start>": ["This is <strings> and my phone number is <phone-number>"],
    "<strings>": ["<string-block>"],
    "<string-block>": ["<string><string><string><string><string>"],
    "<string>": ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],

    "<phone-number>": ["<digits>"],
    "<digits>": ["<digit-block>-<digit-block>-<digit-block>"],
    "<digit-block>": ["<digit><digit><digit>"]
}

if __name__ == "__main__":
	for i in range(10):
         print(simple_grammar_fuzzer(grammar=Fake_Name, max_nonterminals=10))

HTML_GRAMMAR = {
    "<start>": ["<xml-tree>"],
    "<xml-tree>": ["<<id>><xml-content></<id>>"],
    "<xml-content>": ["Text", "<xml-tree>"],
    "<id>": ["<letter>", "<id><letter>"],
    "<letter>": ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
}

g = GrammarFuzzer(HTML_GRAMMAR)
g.fuzz()
