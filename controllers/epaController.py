# -*- coding: utf-8 -*-

from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
from marshmallow.utils import missing

from controllers.epa import cas_to_epa
from controllers.defs import VAF, VVF

class epaController(Resource):
    args = {
        'texto': fields.Str(
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
        ),
    }

    @use_kwargs(args)
    def get(self, texto, vaf, vvf):
        if vaf == missing: vaf = VAF
        if vvf == missing: vvf = VVF
        return {texto: cas_to_epa(texto, vaf=vaf, vvf=vvf)}
    
    # def post(self):
    #     return {"response" : "hello post"}

    # def put(self):
    #     return {"response" : "hello put"}

    # def delete(self):
    #     return {"response" : "hello delete"}
