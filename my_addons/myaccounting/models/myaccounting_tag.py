from odoo import models,fields,api
from datetime import timedelta
from odoo import models,fields,api
from datetime import timedelta

class MyaccountingPropertyType(models.Model):
    _name = 'myaccounting.tag'
    _description = '会计标签'
    color = fields.Integer(string="标签颜色", default=10)

    name = fields.Char(string="标签名称")
    _sql_constraints = [
        ('name_uniq', 'unique(name)', '标签名称必须唯一！'),
    ]
