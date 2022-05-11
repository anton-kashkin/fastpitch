""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from .cmudict import valid_symbols


# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in valid_symbols]

_russian_phonemes = ["a" ,'a+','b','bʲ','d','dʲ','d͡b','d͡bʲ','d͡z','d͡zʲ',
'e','e+','f','fʲ','i','i+','j','k','kʲ','k͡x','k͡xʲ','lʲ','lˠ','m','mʲ',
'm̥','n','nʲ','n͡m','o','o+','p','pʲ','r','rʲ','s','sʲ','t','tʲ','t͡p',
't͡pʲ','t͡s','t͡sʲ','t͡ɕ','u','u+','v','vʲ','x','xʲ','z','zʲ','æ+',
'ɐ','ɕ','ɖ͡ʐ','ə','ə+','ɛ','ɛ+','ɡ','ɡʲ','ɣ','ɨ','ɨ+','ɪ','ɵ','ɵ+',
'ʂ','ʈ͡ʂ','ʉ','ʉ+','ʊ','ʐ','ʑ']

_russial_graphemes = ['Ё','А','А0','Б','В','Г','Д','Е','Е0','Ж','З','И','И0','Й','К','Л','М','Н','О','О0','П','Р','С','Т','У','У0','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ы0','Ь','Э','Э0','Ю','Ю0','Я','Я0','а','а0',
'б','в','г','д','е','е0','ж','з','и','и0','й','к','л','м','н','о',
'о0','п','р','с','т','у','у0','ф','х','ц','ч','ш','щ','ъ','ы','ы0','ь','э',
'э0','ю','ю0','я','я0','ё']

def get_symbols(symbol_set='english_basic'):
    if symbol_set == 'russian_graphemes':
        _pad = '_'
        _punctuation = '?.'
        _pauses = ['<space>', '#','%']
        symbols = list(_pad + _punctuation) + _pauses + _russial_graphemes
    elif symbol_set == 'russian_phonemes':
        _pad = <TODO: padding symbol>
        _punctuation = '!?.'
        _pauses = ['_', '#0', '#1', '#2', '#3', '#4', '#5']
        symbols = list(_pad + _punctuation) + _pauses + _russian_phonemes  
    elif symbol_set == 'english_basic':
        _pad = '_'
        _punctuation = '!\'(),.:;? '
        _special = '-'
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    elif symbol_set == 'english_basic_lowercase':
        _pad = '_'
        _punctuation = '!\'"(),.:;? '
        _special = '-'
        _letters = 'abcdefghijklmnopqrstuvwxyz'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    elif symbol_set == 'english_expanded':
        _punctuation = '!\'",.:;? '
        _math = '#%&*+-/[]()'
        _special = '_@©°½—₩€$'
        _accented = 'áçéêëñöøćž'
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        symbols = list(_punctuation + _math + _special + _accented + _letters) + _arpabet
    else:
        raise Exception("{} symbol set does not exist".format(symbol_set))

    return symbols


def get_pad_idx(symbol_set='english_basic'):
    if symbol_set in {'english_basic', 'english_basic_lowercase', 'russian_graphemes', 'russian_phonemes'}:
        return 0
    else:
        raise Exception("{} symbol set not used yet".format(symbol_set))
