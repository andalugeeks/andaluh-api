# -*- coding: utf-8 -*-

from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

import andaluh
from andaluh.defs import VAF, VVF

class andaluhController(Resource):
    args = {
        'spanish': fields.Str(
            type_=unicode,
            required=True
        ),
        'vaf': fields.Str(
            type_=unicode,
            required=False
        ),
        'vvf': fields.Str(
            type_=unicode,
            required=False
        )
    }

    @use_kwargs(args)
    def get(self, spanish, vaf=VAF, vvf=VVF):
        return {
            "spanish": spanish,
            "andaluh": andaluh.epa(spanish, vaf=vaf, vvf=vvf),
            "rules": {
                "vaf": vaf,
                "vvf": vvf
            }
        }
