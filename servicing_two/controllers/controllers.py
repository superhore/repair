# -*- coding: utf-8 -*-
from odoo import http

# class ServicingTwo(http.Controller):
#     @http.route('/servicing_two/servicing_two/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/servicing_two/servicing_two/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('servicing_two.listing', {
#             'root': '/servicing_two/servicing_two',
#             'objects': http.request.env['servicing_two.servicing_two'].search([]),
#         })

#     @http.route('/servicing_two/servicing_two/objects/<model("servicing_two.servicing_two"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('servicing_two.object', {
#             'object': obj
#         })