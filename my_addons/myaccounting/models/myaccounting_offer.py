from odoo import models, fields, api
from datetime import timedelta

class MyaccountingPropertyOffer(models.Model):
    _name = 'myaccounting.offer'
    _description = '科目余额'


    date = fields.Date(string="日期",readonly=True, default=fields.Date.today)
    voucher_number = fields.Char(string="凭证号", copy=False)
    abstract = fields.Char(string="摘要")
    coding = fields.Char(string="科目编码")
    subject_name = fields.Char(string="科目名称")
    initial_balance_debtor = fields.Float(string="期初余额(借方)", copy=False)
    initial_balance_creditor = fields.Float(string="期初余额(贷方)", copy=False)
    current_period_debtor = fields.Float(string="本期发生额(借方)", copy=False)
    current_period_creditor = fields.Float(string="本期发生额(贷方)", copy=False)
    year_to_date_debtor = fields.Float(string="本年累计发生额(借方)", compute='_compute_year_to_date', store=True)
    year_to_date_creditor = fields.Float(string="本年累计发生额(贷方)", compute='_compute_year_to_date', store=True)
    final_balance_debtor = fields.Float(string="期末余额(借方)", compute='_compute_final_balance', store=True)
    final_balance_creditor = fields.Float(string="期末余额(贷方)", compute='_compute_final_balance', store=True)
    balance_type = fields.Selection([('debtor', '借'), ('creditor', '贷'), ('balance', '余额')], string='方向')
    sequence = fields.Integer(string="序号", default=1)
    coding_parent = fields.One2many('account.move.test', 'coding', string="上级科目编码")

    # tags = fields.Many2many(
    #     'myaccounting.tag',
    #     string='标签',
    #     help='与科目相关的标签'
    # )
    #
    # # 如果需要显示标签的名称，可以添加一个计算字段
    # tag_names = fields.Char(
    #     string='标签名称',
    #     compute='_compute_tag_names',
    #     store=True
    # )

    # @api.depends('tags')
    # def _compute_tag_names(self):
    #     for record in self:
    #         # 将所有标签的名称拼接成字符串
    #         record.tag_names = ', '.join(tag.name for tag in record.tags)
    @api.depends('current_period_debtor', 'current_period_creditor')
    def _compute_year_to_date(self):
        for record in self:
            # 假设本年累计发生额 = 期初余额 + 本期发生额
            record.year_to_date_debtor = record.initial_balance_debtor + record.current_period_debtor
            record.year_to_date_creditor = record.initial_balance_creditor + record.current_period_creditor

    @api.depends('year_to_date_debtor', 'year_to_date_creditor')
    def _compute_final_balance(self):
        for record in self:
            # 假设期末余额 = 本年累计发生额
            record.final_balance_debtor = record.year_to_date_debtor
            record.final_balance_creditor = record.year_to_date_creditor

    @api.model
    def get_total_summary(self):
        # 查询所有记录并计算汇总
        total_debtor = self.search([]).mapped('final_balance_debtor')
        total_creditor = self.search([]).mapped('final_balance_creditor')
        return {
            'total_debtor': sum(total_debtor),
            'total_creditor': sum(total_creditor)
        }

