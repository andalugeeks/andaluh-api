#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

import re
import subprocess
from exceptions import Exception

VOWELS = u'aeiou'
VOWELS_TILDE = u'áéíóú'
VOWELS_CIRCUMFLEX = u'âêîôû'
VOWELS_UP = u'AEIOU'
VOWELS_TILDE_UP = u'ÁÉÍÓÚ' 
VOWELS_CIRCUMFLEX_UP = u'ÂÊÎÔÛ'

# Pre calculation of vowel groups and its variants with accents. Useful for further search & replacement
VOWELS_ALL = VOWELS + VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_NOTILDE = VOWELS + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_TILDE = VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP

# EPA character for Voiceless alveolar fricative /s/ https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = u'ç'
VAF_UP = u'Ç'

# Auxiliary functions
def get_vowel_circumflex(vowel):

    # If no tilde, replace with circumflex
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i: i+1][0]

    # If vowel with tilde, leave it as it is
    elif vowel and vowel in VOWELS_ALL_TILDE:
        return vowel

    # You shouldn't call this method with a non vowel
    else:
        raise EPAError('Not a vowel', vowel)

def is_stressed_syllable(word):
    syllables = subprocess.check_output(['./contrib/SeparadorDeSilabas.exe', word])
    word, n_syllab, accent_syllab, accent = syllables.split(',')
    return n_syllab == accent_syllab

# EPA replacement functions
def h_rules(text):
    """Supress mute /h/"""

    text = re.sub(ur'(?<!c)h', '', text, flags=re.IGNORECASE)
    return text

def x_rules(text):
    """Replacement rules for /ks/ with EPA VAF"""

    def replace_with_case(match):
        whitespaces = match.group(1)
        x_char = match.group(2)

        if x_char.islower():
            return whitespaces + VAF
        else:
            return whitespaces + VAF_UP

    def replace_intervowel_with_case(match):
        prev_char = match.group(1)
        x_char = match.group(2)
        next_char = match.group(3)

        prev_char = get_vowel_circumflex(prev_char)

        if x_char.isupper():
            return prev_char + VAF_UP*2 + next_char
        else:
            return prev_char + VAF*2 + next_char

    # If the text begins with /ks/
    if text[0] == "X": text = VAF_UP + text[1:]
    if text[0] == "x": text = VAF + text[1:]

    # If the /ks/ sound is between vowels
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(x)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)', replace_intervowel_with_case, text, flags=re.IGNORECASE)

    # Every word starting with /ks/
    text = re.sub(ur'([\W]+)(x|X)', replace_with_case, text, flags=re.IGNORECASE)

    return text

def ch_rules(text):
    """Replacement rules for /∫/ (voiceless postalveolar fricative)"""

    def replace_with_case(match):
        c_char = match.group(1)

        if c_char.islower():
            return 'x'
        else: 
            return 'X'

    text = re.sub(ur'(c)(h)', replace_with_case, text, flags=re.IGNORECASE)
    return text

def gj_rules(text):
    """Replacing /x/ (voiceless postalveolar fricative) with /h/"""
    # G,J + vowel replacement
    text = re.sub(ur'(g|j)(e|i|é|í|E|I|É|Í)', ur'h\2', text)
    text = re.sub(ur'(G|J)(e|i|é|í|E|I|É|Í)', ur'H\2', text)
    text = re.sub(ur'(j)(a|o|u|á|ó|ú|A|O|U|Á|Ó|Ú)', ur'h\2', text)
    text = re.sub(ur'(J)(a|o|u|á|ó|ú|A|O|U|Á|Ó|Ú)', ur'H\2', text)

    # GUE,GUI replacement
    text = re.sub(ur'(gu|gU)(e|i|é|í|E|I|É|Í)', ur'g\2', text)
    text = re.sub(ur'(Gu|GU)(e|i|é|í|E|I|É|Í)', ur'G\2', text)

    # GÜE,GÜI replacement
    text = re.sub(ur'(g|G)(ü)(e|i|é|í|E|I|É|Í)', ur'\1u\3', text)
    text = re.sub(ur'(g|G)(Ü)(e|i|é|í|E|I|É|Í)', ur'\1U\3', text)

    return text

def v_rules(text):
    """Replacing all /v/ (Voiced labiodental fricative) with /b/"""

    def replace_with_case(match):
        n_char = match.group(1)
        v_char = match.group(2)

        if n_char.islower() and v_char.islower():
            return 'mb'
        if n_char.isupper() and v_char.isupper():
            return 'MB'
        if n_char.isupper() and v_char.islower():
            return 'Mb'
        else: 
            return 'mB'

    # NV -> NB -> MB (i.e.: envidia -> embidia)
    text = re.sub(ur'(n)(v)', replace_with_case, text, flags=re.IGNORECASE)

    # v -> b
    text = re.sub(ur'v', ur'b', text)
    text = re.sub(ur'V', ur'B', text)

    return text

def ll_rules(text):
    """Replacing /ʎ/ (digraph ll) with Greek Y for /ʤ/ sound (voiced postalveolar affricate)"""

    def replace_with_case(match):
        l1_char = match.group(1)

        if l1_char.islower():
            return 'y'
        else:
            return 'Y'

    text = re.sub(ur'(l)(l)', replace_with_case, text, flags=re.IGNORECASE)
    return text

def l_rules(text):
    """Rotating /l/ with /r/"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return 'r' + next_char
        else: 
            return 'R' + next_char

    text = re.sub(ur'(l)(b|c|g|s|d|f|g|h|m|n|p|q|r|t|x)', replace_with_case, text, flags=re.IGNORECASE)
    return text

def vaf_rules(text):
    """Replacing Voiceless alveolar fricative (vaf) /s/ /θ/ with EPA's ç/Ç"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return VAF + next_char
        else:
            return VAF_UP + next_char

    text = re.sub(ur'(z|s)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)', replace_with_case, text, flags=re.IGNORECASE)
    text = re.sub(ur'(c)(e|i|é|í)', replace_with_case, text, flags=re.IGNORECASE)

    return text

def digraph_rules(text):
    """Replacement of consecutive consonant with EPA VAF"""

    def replace_with_case(match):
        vowel_char = match.group(1)
        # to_drop_char = match.group(2) # We do not need to calculate it anyway ...
        digraph_char = match.group(3)

        return get_vowel_circumflex(vowel_char) + digraph_char*2

    # TODO: Excepciones de la regla del dígrafo.
    #   - Doble ele -> Aislante - Aîl-lante.
    #   - Casos que acabarían en doble erre pero no ocurre porque las dos consonantes forman fonema:
    #       - No genera dígrafo con 'ele': bl, cl, fl, gl, pl
    #       - No genera dígrafo con 'erre': br, cr, dr, fr, pr, tr
    #   - Raíz psico / psica no aplica. Sacar de regla del dígrafo y sencillamente quitar la "pé" y continuar con el algoritmo.
    #   - Dígrafo especial (vocal)MN => (vôcal)NN. Ej: amnesia => ânneçia.
    #   - No-dígrafo (vocal)NM => relajación de la 'n' en 'm' sin espirar la vocal. Ej. conmemorar => commemorâh
    #   - Trígrafo: Prefifo ABS(cons)/TRANS(cons) (extendido a (vocal)BS(cons)|TR(vocal)NS(const) se pierden dos consonantes.
    #       Ejemplo: Abstracto => Âttrâtto. Transporte => Trâpporte.
    #   - Reglas LST/RST (intersticial / solsticio / superstición / cárstico). La L rota con R. Se cae la S. Ej: interttiçiâh, çorttiçio.
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(b|c|d|f|g|j|p|s|t|x|z)(b|c|ç|d|f|g|h|l|m|n|p|q|r|t|x|y)', replace_with_case, text, flags=re.IGNORECASE)

    return text

def word_ending_rules(text):
    """Replacement of word endings"""

    stressed_syllable = {
        u'ad':u'á', u'ed':u'é', u'id':u'îh', u'od':u'ôh', u'ud':u'ûh',
        u'aD':u'á', u'eD':u'é', u'iD':u'îH', u'oD':u'ôH', u'uD':u'ûH',
        u'AD':u'Á', u'ED':u'É', u'ID':u'ÎH', u'OD':u'ÔH', u'UD':u'ÛH',
        u'Ad':u'Á', u'Ed':u'É', u'Id':u'Îh', u'Od':u'Ôh', u'Ud':u'Ûh'
    }
    unstressed_syllable = {
        u'ad':u'â', u'ed':u'ê', u'id':u'î', u'od':u'ô', u'ud':u'û',
        u'aD':u'â', u'eD':u'ê', u'iD':u'î', u'oD':u'ô', u'uD':u'û',
        u'AD':u'Â', u'ED':u'Ê', u'ID':u'Î', u'OD':u'Ô', u'UD':u'Û',
        u'Ad':u'Â', u'Ed':u'Ê', u'Id':u'Î', u'Od':u'Ô', u'Ud':u'Û'
    }

    def replace_with_case(match):
        word = match.group(0)
        prefix = match.group(1)
        suffix = match.group(2)
        
        # TODO: Replace syllablification with the following fixed rules:
        # - Palabras que acaban en (vocal)(l|z|r) ... si hay tilde en el resto de la palabra, no es aguda (unstressed).
        # - Palabras que acaban en (vocal)(d) ... si hay tilde en el resto de la palabra, no es aguda (unstressed).
        # - Palabras que acaban en (vocal sin tildar)(s) ... unstressed.
        # - Palabras que acaban en (vocal tildada)(s) ... stressed.
        if is_stressed_syllable(word):
            return prefix + stressed_syllable[suffix]
        else:
            return prefix + unstressed_syllable[suffix]

    text = re.sub(ur'\b(\w*?)(ad|ed|id|od|ud)\b', replace_with_case, text, flags=re.IGNORECASE)

    return text

# Main function
def cas_to_epa(text):
    # text = unicode(text, 'utf-8')
    text = h_rules(text)
    text = x_rules(text)
    text = ch_rules(text)
    text = gj_rules(text)
    text = v_rules(text)
    text = ll_rules(text)
    text = l_rules(text)
    text = vaf_rules(text)
    text = digraph_rules(text)
    # text = word_ending_rules(text)

    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors