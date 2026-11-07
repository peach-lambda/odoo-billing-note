from odoo import models, fields, api, _

class CustomerBillingNote(models.Model):
    _name = 'customer.billing.note'
    _description = 'Customer Billing Note'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, name desc'

    name = fields.Char(string='Billing Note Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    date = fields.Date(string='Billing Date', default=fields.Date.context_today, required=True, tracking=True)
    due_date = fields.Date(string='Payment Due Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    invoice_ids = fields.Many2many(
        'account.move', 
        'billing_note_invoice_rel', 
        'billing_note_id', 
        'move_id', 
        string='Invoices',
        domain="[('partner_id', '=', partner_id), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]"
    )
    
    currency_id = fields.Many2one('res.currency', string='Currency', related='partner_id.currency_id', store=True, readonly=True)
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_totals', store=True, currency_field='currency_id')
    amount_residual = fields.Monetary(string='Amount Due', compute='_compute_totals', store=True, currency_field='currency_id')
    note = fields.Text(string='Terms & Conditions')

    @api.depends('invoice_ids', 'invoice_ids.amount_total', 'invoice_ids.amount_residual')
    def _compute_totals(self):
        for record in self:
            record.total_amount = sum(inv.amount_total for inv in record.invoice_ids)
            record.amount_residual = sum(inv.amount_residual for inv in record.invoice_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('customer.billing.note') or _('BN/%s') % fields.Date.today().year
        return super(CustomerBillingNote, self).create(vals_list)

    def action_send(self):
        self.write({'state': 'sent'})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
