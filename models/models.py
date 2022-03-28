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

    partner_ref = fields.Char(
        string='Vendor Invoice No.',
        required=False)


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
    
class AccountPaymentMethodLine(models.Model):
    _inherit = 'account.payment.method.line'
    
    charge_include = fields.Boolean(
        string='Charge Include', 
        required=False)
    rate = fields.Float(
        string='Rate', 
        required=False)
    max_fee = fields.Monetary(currency_field='currency_id', readonly=False,
                              string='Maximum Fee')
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
                                  compute='_compute_currency_id',
                                  help="The payment's currency.")

    @api.depends('journal_id')
    def _compute_currency_id(self):
        for wizard in self:
            wizard.currency_id = wizard.journal_id.currency_id or wizard.company_id.currency_id

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    pos_fee = fields.Monetary(currency_field='currency_id', store=True, readonly=False,
                              string='POS Fee')
    amount_pluspos = fields.Monetary(currency_field='currency_id', store=True, readonly=False, string='Amount Plus POS fee',
                                     compute='_compute_newamount')


    @api.onchange('payment_method_line_id')
    def pos_charge(self):
        for rec in self:
            if rec.payment_method_line_id.charge_include:
                pos_fee = rec.payment_method_line_id.rate /100 * self.amount
                if pos_fee < rec.payment_method_line_id.max_fee:
                    self.pos_fee = pos_fee
                else:
                    self.pos_fee = rec.payment_method_line_id.max_fee
            else:
                self.pos_fee = 0

    @api.depends('pos_fee')
    def _compute_newamount(self):
        for rec in self:
            self.amount_pluspos = rec.amount + rec.pos_fee


    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount_pluspos,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals

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
