# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

import andaluh
from andaluh.defs import VAF, VVF

parser = reqparse.RequestParser()
parser.add_argument('spanish', type=str, required=True, help='Spanish text to transliterate')
parser.add_argument('vaf', type=str, required=False, choices=('ç','z','s','h'), help='Use only ç, z, s, h to mark çeçeo, zezeo, seseo or heheo.')
parser.add_argument('vvf', type=str, required=False, choices=('h','j'), help='Use only h or j for /x/ sound.')
parser.add_argument('escapeLinks', type=str, choices=('True','true', 'False', 'false'), required=False, help='Use true to escape URL, hashtag and mentions from transliteration, otherwise false.')

class andaluhController(Resource):
    def get(self):
        args = parser.parse_args()
        spanish = args['spanish']
        vaf = args['vaf'] or VAF
        vvf = args['vvf'] or VVF
        escapeLinks = True if args['escapeLinks'] in ['True', 'true'] else False

        return {
            "spanish": spanish,
            "andaluh": andaluh.epa(spanish, vaf=vaf, vvf=vvf, escape_links=escapeLinks),
            "rules": {
                "vaf": vaf,
                "vvf": vvf,
                "escapeLinks": escapeLinks
            }
        }
