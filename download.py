import nltk
import ssl

"""
This file downloads the wordnet extension of nltk.
It can not be downloaded with pip.
It looks complicated because the NLTK server can respond badly on a wrong ssl certificate,
so this script disables the SSL check.
"""
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')