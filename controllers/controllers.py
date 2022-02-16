# -*- coding: utf-8 -*-
# from odoo import http


# class DrinksCustom(http.Controller):
#     @http.route('/drinks_custom/drinks_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/drinks_custom/drinks_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('drinks_custom.listing', {
#             'root': '/drinks_custom/drinks_custom',
#             'objects': http.request.env['drinks_custom.drinks_custom'].search([]),
#         })

#     @http.route('/drinks_custom/drinks_custom/objects/<model("drinks_custom.drinks_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('drinks_custom.object', {
#             'object': obj
#         })
