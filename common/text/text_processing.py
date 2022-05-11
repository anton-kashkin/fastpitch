""" adapted from https://github.com/keithito/tacotron """
import re
import numpy as np
from . import cleaners
from .symbols import get_symbols
from . import cmudict
from .numerical import _currency_re, _expand_currency


#########
# REGEX #
#########

# Regular expression matching text enclosed in curly braces for encoding
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

# Regular expression matching words and not words
_words_re = re.compile(r"([a-zA-ZÀ-ž]+['][a-zA-ZÀ-ž]{1,2}|[a-zA-ZÀ-ž]+)|([{][^}]+[}]|[^a-zA-ZÀ-ž{}]+)")

# Regular expression separating words enclosed in curly braces for cleaning
_arpa_re = re.compile(r'{[^}]+}|\S+')


class TextProcessing(object):
    def __init__(self, symbol_set, cleaner_names, p_arpabet=0.0,
                 handle_arpabet='word', handle_arpabet_ambiguous='ignore',
                 expand_currency=False):
        self.symbols = get_symbols(symbol_set)
        print(f'symbols: {self.symbols}')
        self.cleaner_names = cleaner_names

        # Mappings from symbol to numeric ID and vice versa:
        self.symbol_to_id = {s: i for i, s in enumerate(self.symbols)}
        self.id_to_symbol = {i: s for i, s in enumerate(self.symbols)}
        self.expand_currency = expand_currency

        # cmudict
        self.p_arpabet = p_arpabet
        self.handle_arpabet = handle_arpabet
        self.handle_arpabet_ambiguous = handle_arpabet_ambiguous


    def text_to_sequence(self, text):
        sequence = []
        sequence += self.symbols_to_sequence(text)
        return sequence
        
    def sequence_to_text(self, sequence):
        result = ''
        for symbol_id in sequence:
            if symbol_id in self.id_to_symbol:
                s = self.id_to_symbol[symbol_id]
                # Enclose ARPAbet back in curly braces:
                if len(s) > 1 and s[0] == '@':
                    s = '{%s}' % s[1:]
                result += s
        return result.replace('}{', ' ')

    def clean_text(self, text):
        for name in self.cleaner_names:
            cleaner = getattr(cleaners, name)
            if not cleaner:
                raise Exception('Unknown cleaner: %s' % name)
            text = cleaner(text)

        return text

    def symbols_to_sequence(self, symbols):
        return [self.symbol_to_id[s] for s in symbols if s in self.symbol_to_id]

    def arpabet_to_sequence(self, text):
        return self.symbols_to_sequence(['@' + s for s in text.split()])

    def get_arpabet(self, word):
        arpabet_suffix = ''

        if word.lower() in cmudict.heteronyms:
            return word

        if len(word) > 2 and word.endswith("'s"):
            arpabet = cmudict.lookup(word)
            if arpabet is None:
                arpabet = self.get_arpabet(word[:-2])
                arpabet_suffix = ' Z'
        elif len(word) > 1 and word.endswith("s"):
            arpabet = cmudict.lookup(word)
            if arpabet is None:
                arpabet = self.get_arpabet(word[:-1])
                arpabet_suffix = ' Z'
        else:
            arpabet = cmudict.lookup(word)

        if arpabet is None:
            return word
        elif arpabet[0] == '{':
            arpabet = [arpabet[1:-1]]

        # XXX arpabet might not be a list here
        if type(arpabet) is not list:
            return word

        if len(arpabet) > 1:
            if self.handle_arpabet_ambiguous == 'first':
                arpabet = arpabet[0]
            elif self.handle_arpabet_ambiguous == 'random':
                arpabet = np.random.choice(arpabet)
            elif self.handle_arpabet_ambiguous == 'ignore':
                return word
        else:
            arpabet = arpabet[0]

        arpabet = "{" + arpabet + arpabet_suffix + "}"

        return arpabet

    def encode_text(self, text: list):

        text_encoded = self.text_to_sequence(text)

        # if return_all:
        #     return text_encoded, text_clean, text_arpabet

        return text_encoded
