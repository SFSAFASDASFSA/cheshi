from odoo import models, fields, api
from datetime import timedelta


class MyaccountingProperty(models.Model):
    _name = 'myaccounting.property'
    _description = 'Real Myaccounting'
    _order = 'sequence desc'

    name = fields.Char(string="科目名称")
    coding = fields.Many2one(string="科目编码", copy=False)
    year = fields.Date(string="会计年度")
    period = fields.Selection([
        ('year', '年度'),
        ('half', '半年'),
        ('quarter', '季度'),
        ('once', '一次性')
    ], string='期间')
    abstract = fields.Char(string="摘要")
    borrowing_balance = fields.Float(string="借方金额", copy=False)
    loan_amount = fields.Float(string="贷方金额", copy=False)
    balance_type = fields.Selection([
        ('debtor', '借方'),
        ('creditor', '贷方'),
        ('balance', '余额')
    ], string='方向')
    state = fields.Selection([
        ('normal', '正常'),
        ('abnormal', '异常'),
        ('locked', '锁定'),
        ('unfilled_order', '未完成')
    ], string='状态')
    voucher_number = fields.Many2one(string="凭证号", copy=False)
    money_lender_id = fields.Many2one('res.partner', string='贷方者')
    borrower_id = fields.Many2one('res.partner', string='借方者')
    tag_ids = fields.Many2many('myaccounting.tag', string='会计标签')
    total_price = fields.Float(string="余额", store=True, compute='_compute_total_price')
    sequence = fields.Integer(string="序号", default=1)


    # 新增字段：期间类型（如期初余额、本期合计、本年累计）
    period_type = fields.Selection([
        ('initial', '期初余额'),
        ('current', '本期合计'),
        ('annual', '本年累计')
    ], string='期间类型', required=True)

    _sql_constraints = [
        ('voucher_number_uniq', 'unique(voucher_number)', '凭证号必须唯一！'),
    ]

    @api.depends('borrowing_balance', 'loan_amount')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.borrowing_balance + record.loan_amount

    @api.onchange('borrowing_balance')
    def _onchange_borrowing_balance(self):
        if self.borrowing_balance > 0:
            self.borrowing_balance = -self.borrowing_balance

    def do_action_locked(self):
        for record in self:
            if record.state != 'abnormal':
                record.state = 'locked'

    def do_action_abnormal(self):
        for record in self:
            if record.state != 'locker':
                record.state = 'abnormal'