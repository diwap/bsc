# -*- coding: utf-8 -*-
from odoo import http

# class Bsc(http.Controller):
#     @http.route('/bsc/bsc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bsc/bsc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bsc.listing', {
#             'root': '/bsc/bsc',
#             'objects': http.request.env['bsc.bsc'].search([]),
#         })

#     @http.route('/bsc/bsc/objects/<model("bsc.bsc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bsc.object', {
#             'object': obj
#         })