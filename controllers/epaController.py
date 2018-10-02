# -*- coding: utf-8 -*-

from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from controllers.epa import cas_to_epa

class epaController(Resource):
    args = {
        'texto': fields.Str(
            type_=unicode,
            required=True
        ),
    }

    @use_kwargs(args)
    def get(self, texto):
        return {
            texto: cas_to_epa(texto),
            "reglas_activas": [
                'h',
                'x',
                'ch',
                'gj',
                'v',
                'll',
                'l',
                'ç',
                'digrafos'
            ]}
    
    # def post(self):
    #     return {"response" : "hello post"}

    # def put(self):
    #     return {"response" : "hello put"}

    # def delete(self):
    #     return {"response" : "hello delete"}
