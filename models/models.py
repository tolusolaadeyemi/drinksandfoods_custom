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
    # facebook_handle = fields.Char(string='FacebookHandle')
    # instagram_handle = fields.Char(string='InstagramHandle')
    # credit_limit = fields.Float(
    #     string='Credit limit',
    #     required=False)
    # @api.onchange('barcode_scan')
    # def _onchange_barcode_scan(self):
    #     product_rec = self.env['product.product']
    #     if self.barcode_scan:
    #         product = product_rec.search([('barcode', '=', self.barcode_scan)])
    #         self.product_id = product.id

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         record_name = record.name + ' - ' + record.member_no
    #         result.append((record.id, record_name))
    #     return result

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    current_sale_price = fields.Float(string='Current Price', related='product_id.list_price')
    new_sale_price = fields.Float(string='New Price')

    # @api.model
    # def create(self, vals):
    #     result = super(PurchaseOrderLine, self).create(vals)
    #     if 'new_sale_price' in vals:
    #         product = self.product_id.id
    #         new_p = self.env('product.template').search([('product_id'.id, '=', record.id)], limit=1)
    #         if new_p:
    #             new_p['list_price'] = self.new_sale_price
    #
    #         # new_price = {
    #         #     "list_price" : self.new_sale_price
    #         # }
    #

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def update_price(self):
        for line in self.order_line:
            if line.new_sale_price:
                line.product_id.list_price = line.new_sale_price


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    description_purchase = fields.Text(
        string="Description_purchase",
        required=False, related='description_sale' )


    def name_get(self):
        result = []
        for rec in self:
            rec_name = rec.description_sale
            result.append((rec.id, rec_name))
        return result

class ProductProduct(models.Model):
    _inherit = 'product.product'


    def name_get(self):
        result = []
        for rec in self:
            rec_name = str(rec.brand_id.name) + ' ' + rec.name
            result.append((rec.id, rec_name))
        return result

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
