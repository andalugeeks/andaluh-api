# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

import andaluh
from andaluh.defs import VAF, VVF
from andaluh_verbs import Conjugador

parser = reqparse.RequestParser()
parser.add_argument('spanish', type=str, location='args', required=True, help='Spanish text to transliterate')
parser.add_argument('vaf', type=str, location='args', required=False, choices=('ç','z','s','h'), help='Use only ç, z, s, h to mark çeçeo, zezeo, seseo or heheo.')
parser.add_argument('vvf', type=str, location='args', required=False, choices=('h','j'), help='Use only h or j for /x/ sound.')
parser.add_argument('escapeLinks', type=str, location='args', choices=('True','true', 'False', 'false'), required=False, help='Use true to escape URL, hashtag and mentions from transliteration, otherwise false.')
parser.add_argument('conjugate', type=str, location='args', choices=('True','true', 'False','false'), required=False, help='Use true to return verb conjugation from andaluh-verbs.')

class andaluhController(Resource):
    def get(self):
        args = parser.parse_args()
        spanish = args['spanish']
        vaf = args['vaf'] or VAF
        vvf = args['vvf'] or VVF
        escapeLinks = True if args['escapeLinks'] in ['True', 'true'] else False
        conjugate_flag = True if args['conjugate'] in ['True', 'true'] else False

        response = {
            "spanish": spanish,
            "andaluh": andaluh.epa(spanish, vaf=vaf, vvf=vvf, escape_links=escapeLinks),
            "rules": {
                "vaf": vaf,
                "vvf": vvf,
                "escapeLinks": escapeLinks,
                "conjugate": conjugate_flag
            }
        }

        if conjugate_flag:
            try:
                conjugator = Conjugador(spanish)
                response["conjugation"] = conjugator.conjugate()
            except Exception as exc:
                response["conjugation_error"] = str(exc)

        return response
