from reportlab.graphics.transform import inverse

from odoo import models, fields, api
from datetime import timedelta
from odoo.fields import Date as fields_Date

class AccountMove(models.Model):
    _name = 'account.move.test'
    _description = '明细分类账'


    date = fields.Date(string="日期",  readonly=True, default=fields.Date.today)
    voucher_number = fields.Char(string="凭证号",copy=False)
    abstract = fields.Char(string="摘要")
    debtor = fields.Float(string="借方金额", copy=False)
    creditor = fields.Float(string="贷方金额", copy=False)
    balance_type = fields.Selection([('debtor', '借方'), ('creditor', '贷方'), ('balance', '余额')], string='方向')
    balance = fields.Float(string="余额")
    sequence = fields.Integer(string="序号", default=1)
    coding = fields.Many2one('myaccounting.offer',string="科目编码")


    # 新增字段：用于存储期初余额
    # initial_balance = fields.Float(string="期初余额", compute='_compute_initial_balance', store=True)
    # 新增字段：用于存储本期合计
    # current_period_total = fields.Float(string="本期合计", compute='_compute_current_period_total', store=True)

    # @api.depends('date', 'debtor', 'creditor')
    # def _compute_initial_balance(self):
    #     for record in self:
    #         # 计算期初余额逻辑
    #         # 假设期初余额是当前记录之前的所有记录的余额总和
    #         initial_records = self.search([('id', '<', record.id), ('coding', '=', record.coding)])
    #         record.initial_balance = sum(initial_records.mapped('balance'))

    # @api.depends('date', 'debtor', 'creditor')
    # def _compute_initial_balance(self):
    #     for record in self:
    #         # 检查 record.id 是否是临时 ID 或无效 ID
    #         if isinstance(record.id, str) and (record.id.startswith('NewId') or not record.id.isdigit()):
    #             record.initial_balance = 0.0
    #         else:
    #             # 确保 record.id 是整数
    #             try:
    #                 record_id = int(record.id)
    #             except (ValueError, TypeError):
    #                 record.initial_balance = 0.0
    #                 continue
    #
    #             # 计算期初余额逻辑
    #             initial_records = self.search([('id', '<', record_id), ('coding', '=', record.coding)])
    #             record.initial_balance = sum(initial_records.mapped('balance'))

    # @api.model
    # def search_panel_select_all_multi_range(self, field_name, **kwargs):
    #     res = self.search_panel_select_multi_range(field_name, **kwargs)
    #     field_range = res['values']
    #     field = self._fields[field_name]
    #     if field.type == 'selection':
    #         return {'values': field_range, }
    #     Comodel = self.env.get(field.comodel_name).with_context(hierarchical_naming=False)
    #     limit = kwargs.get('limit')
    #     enable_counters = kwargs.get('enable_counters')
    #     group_by = kwargs.get('group_by')
    #     field_names = ['display_name']
    #
    #     if group_by:
    #         id_list = [record['id'] for record in field_range]
    #         id_set = set(id_list)
    #         group_set = set([record['group_id'] for record in field_range])
    #         need_add_group_set = group_set - id_set
    #
    #         group_by_field = Comodel._fields[group_by]
    #
    #         field_names.append(group_by)
    #
    #         if group_by_field.type == 'many2one':
    #             def group_id_name(value):
    #                 return value or (False, ("Not Set"))
    #
    #         elif group_by_field.type == 'selection':
    #             desc = Comodel.fields_get([group_by])[group_by]
    #             group_by_selection = dict(desc['selection'])
    #             group_by_selection[False] = ("Not Set")
    #
    #             def group_id_name(value):
    #                 return value, group_by_selection[value]
    #
    #         else:
    #             def group_id_name(value):
    #                 return (value, value) if value else (False, ("Not Set"))
    #
    #         group_list = list(need_add_group_set)
    #         while True:
    #             if need_add_group_set.__len__() == 0:
    #                 break
    #             group_ids = list(need_add_group_set)
    #             need_add_group_set.clear()
    #             comodel_records = Comodel.search_read([('id', 'in', group_ids)], field_names, limit=limit)
    #             for record in comodel_records:
    #                 group_id, group_name = group_id_name(record[group_by])
    #                 values = {
    #                     'id': record['id'],
    #                     'display_name': record['display_name'],
    #                     'group_id': group_id,
    #                     'group_name': group_name, }
    #                 if enable_counters:
    #                     values['__count'] = 0
    #                 field_range.append(values)
    #                 if group_id and group_id not in id_list:
    #                     need_add_group_set.add(group_id)
    #                     group_list.append(group_id)
    #
    #         # 遍历field_range，更新__count的值
    #         def recurve_count(record):
    #             rid = record['id']
    #             for child in field_range:
    #                 if child['group_id'] == rid:
    #                     record['__count'] += recurve_count(child)
    #             return record['__count']
    #
    #         field_dict = {it['id']: it for it in field_range}
    #         field_range = list(field_dict.values())
    #         for record in field_range:
    #             if not record.get('group_id'):
    #                 record['__count'] = recurve_count(record)
    #     return {'values': field_range, }
