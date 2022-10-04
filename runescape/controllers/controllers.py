# -*- coding: utf-8 -*-
# from odoo import http


# class Runescape(http.Controller):
#     @http.route('/runescape/runescape', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/runescape/runescape/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('runescape.listing', {
#             'root': '/runescape/runescape',
#             'objects': http.request.env['runescape.runescape'].search([]),
#         })

#     @http.route('/runescape/runescape/objects/<model("runescape.runescape"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('runescape.object', {
#             'object': obj
#         })
