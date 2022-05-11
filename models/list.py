from odoo import api, fields, models, tools, _
import datetime

class List(models.Model):
    _inherit = 'purchase.order.line'

    x_projects = fields.Char(string=u'项目号',compute='_get_project',store=True)
    x_remark = fields.Char(string=u'备注',compute='_get_remark',store=True)
    x_name = fields.Char(string=u'需求者',compute='_get_name',store=True)
    x_date = fields.Char(string=u'需求时间',compute='_get_date',store=True)

    @api.constrains('order_id')
    def _get_project(self):
        if self.order_id:
            att_model = self.env['stock.move']
            for obj in self:
                query = [("reference","ilike","WH/MO"),("state","!=","done"),("state","!=","cancel"),("state","!=","draft")]
                dd=[]
                for i in att_model.search(query):
                    if obj.product_id ==i.product_id:
                        if i.product_uom_qty==i.forecast_availability:
                            continue
                        else:
                            dd.append(i.raw_material_production_id.product_id.name)
                obj.x_projects=dd

    @api.constrains('order_id')
    def _get_remark(self):
        if self.order_id:
            att_model = self.env['stock.move']
            for obj in self:
                query = [("reference","ilike","WH/MO"),("state","!=","done"),("state","!=","cancel"),("state","!=","draft")]
                dd=[]
                for i in att_model.search(query):
                    if obj.product_id ==i.product_id:
                        if i.product_uom_qty==i.forecast_availability:
                            continue
                        else:
                            dd.append(i.x_remark)
                obj.x_remark=dd
    
    @api.constrains('order_id')
    def _get_name(self):
        if self.order_id:
            att_model = self.env['stock.move']
            for obj in self:
                dd=[]
                query = [("reference","ilike","WH/MO"),("state","!=","done"),("state","!=","cancel"),("state","!=","draft")]
                for i in att_model.search(query):
                    if obj.product_id ==i.product_id:
                        if i.product_uom_qty==i.forecast_availability:
                            continue
                        else:
                            dd.append(i.create_uid.name)
                obj.x_name=dd

    @api.constrains('order_id')
    def _get_date(self):
        if self.order_id:
            att_model = self.env['stock.move']
            for obj in self:
                query = [("reference","ilike","WH/MO"),("state","!=","done"),("state","!=","cancel"),("state","!=","draft")]
                dd=[]
                for i in att_model.search(query):
                    if obj.product_id ==i.product_id:
                        if i.product_uom_qty==i.forecast_availability:
                            continue
                        else:
                            dd.append( datetime.datetime.strftime(i.date, "%Y-%m-%d"))
                obj.x_date=dd
