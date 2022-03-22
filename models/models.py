from odoo import api, models, fields


class SaleOrderLines(models.Model):
    _inherit = 'account.move.line'

    barcode = fields.Char(string='Product Barcode', help="Here you can provide the barcode for the product",
                          related="product_id.barcode")


class Partner(models.Model):
    _inherit = 'res.partner'

    phone = fields.Char(
        string='Phone',
        required=True)
    city = fields.Char(string='City', required=True)
    facebook_handle = fields.Char(string='FacebookHandle')
    instagram_handle = fields.Char(string='InstagramHandle')
    credit_limit = fields.Float(
        string='Credit limit',
        required=False)
    # @api.onchange('barcode_scan')
    # def _onchange_barcode_scan(self):
    #     product_rec = self.env['product.product']
    #     if self.barcode_scan:
    #         product = product_rec.search([('barcode', '=', self.barcode_scan)])
    #         self.product_id = product.id


# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class drinks_custom(models.Model):
#     _name = 'drinks_custom.drinks_custom'
#     _description = 'drinks_custom.drinks_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
