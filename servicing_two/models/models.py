# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class xj_mainten(models.Model):
    _name = "xj.mainten"
    _inherit = ['mail.thread']

    name = fields.Char(string=u'维修付款申请', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', u'草稿'),
        ('confirm', u'待审批'),
        ('validated', u'审批中'),
        ('done', u'完成'),
        ('cancel', u'已驳回'),
    ], string=u'状态', index=True, readonly=True, default='draft', track_visibility='onchange', copy=False)
    application_id = fields.Char(u"单号")
    s_ascriptions = fields.Many2one("wf.station.station", string=u"归属油站",required=True)
    fixed_assets = fields.Char(u"固定资产",required=True)
    applicant = fields.Many2one('res.users', string=u"申请人",index=True,track_visibility="onchange",default=lambda self: self.env.user)
    isshenqing_time = fields.Datetime(u"申请时间")

    isguzhang_info = fields.Many2one("xj.isguzhanginfo",u"故障原因",required=True)

    isweixiu_yusuan = fields.Integer(u"维修预算")
    isjiesuan = fields.Integer(u"结算金额")
    iszhuangtai = fields.Char(u"状态")
    is_thischiliren = fields.Char(compute="_value_pc",string=u"当前处理人")
    isfukuan_bool = fields.Char(u"付款状态")
    islianxi_dianhua = fields.Integer(u"联系电话")

   #   跟下面字段对应fields.many2one('wf.eng.repair.type', string=u'父类型')  xj.repair.re.type
    isweixiu_type = fields.Many2one("xj.wxtype", string=u"维修类型")
    isshenpi_liu = fields.Char(u"选择审批流")

    #  wf.eng.repair.type
    type_son  = fields.Many2one('xj.wxtype', u'维修子类型',required=True)

    repair_sup = fields.One2many("xj.supervise", "sup_repair")

    failure_condition  = fields.Text(u"故障描述")

    repaur_htime = fields.Float(u"维修耗时(天)")
    budgetary_type=fields.Many2one('wf.budget.category', u'预算类型', select=True)
    budget_approval=fields.Many2one('wf.budget', u'预算批复项', select=True)
    maintenance_plan = fields.Text(u"维修方案")

    plan_detailed = fields.One2many("xj.detailed", "detailed_plan", string=u"维修预算明细")

    result_description = fields.Text(u"维修结果意见描述")

    change_type = fields.Selection([('plus', u'加'), ('dec', u'减')], string=u'加/减', required=True)
    change_amount = fields.Float(u'调整金额', required=True)
    # total_amount = fields.Float(compute="_get_total_amount", method=True, readonly=True, string=u'本次结算总金额')

    attachment_one = fields.One2many('ir.attachment', 'res_id', "xj_repair_file_one")
    attachment_two = fields.One2many('ir.attachment', 'res_id', "xj_repair_file_two")
    attachment_there = fields.One2many('ir.attachment', 'res_id', "xj_repair_file_there")
    attachment_fore = fields.One2many('ir.attachment', 'res_id', "xj_repair_file_fore")

    budget_and = fields.Float(u"预算合计", compute="money_add", readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('xj.mainten') or _('New')
        result = super(xj_mainten, self).create(vals)
        return result

    @api.multi
    def money_add(self):

       for rec in self:
           money = 0.0
           for i in rec.plan_detailed:
               money += i.total
           rec.budget_and = money

    @api.multi
    def button_dummy(self):
        return True




    # attachment_repair = fields.One2many('ir.attachment', 'res_id')

    def onchange_budget_type(self, budgetary_type):
        value = {'budget_approval': [('category_id', '=', 0)]}
        if budgetary_type:
            value = {'budget_approval': [('category_id', '=', budgetary_type)]}
        return {'domain': value}

    def onchange_isweixiu_type(self, isweixiu_type):
        value = {'type_son': [('parent_id', '=', 0)]}
        if isweixiu_type:
            value = {'type_son': [('parent_id', '=', isweixiu_type)]}
        return {'domain': value}

    # @api.multi
    # def _get_total_amount(self, cr, uid, ids, field_name, arg, context):
        # res = {}
        #
        # for order in self.browse(cr, uid, ids, context=context):
        #     type = order.change_type
        #     if type == 'plus':
        #         res[order.id] = order.planned_amount + order.change_amount
        #     else:
        #         res[order.id] = order.planned_amount - order.change_amount
        # return res
        # pass



    @api.multi
    def _value_pc(self):
        pass


class xj_detailed(models.Model):
    _name = "xj.detailed"

    detailed_plan = fields.Many2one("xj.mainten")
    name = fields.Char(u"项目")
    unit_price = fields.Float(u"单价", default=0.00)
    number = fields.Float(u"数量", default=0.00)
    total = fields.Float(compute="detailed", string=u"合计")

    @api.multi
    def detailed(self):
        for rec in self:
            rec.total = rec.unit_price * rec.number

class supervise(models.Model):
    _name = "xj.supervise"

    name = fields.Char(u"名称")

    sup_repair = fields.Many2one("xj.mainten")
    wenjian = fields.Binary(u"文件")

    explain = fields.Char(u"说明")



class xj_wxtype(models.Model):
    _name = "xj.wxtype"
    _description = u"维修类型"

    name = fields.Char(string=u"类型名称")
    des = fields.Char(string=u"描述")
    parent_id = fields. Many2one('xj.wxtype', string=u'父类型')


class xj_isguzhanginfo(models.Model):
    _name = "xj.isguzhanginfo"
    _description = u"故障原因"

    name = fields.Char(string=u"故障原因")
    des = fields.Char(string=u"描述")

class file_type(models.Model):
    _name = "xj.file.type"
    _inherit = ['ir.attachment']


    xj_repair_file_one = fields.Many2one("xj.mainten")
    xj_repair_file_two = fields.Many2one("xj.mainten")
    xj_repair_file_there = fields.Many2one("xj.mainten")
    xj_repair_file_fore = fields.Many2one("xj.mainten")









