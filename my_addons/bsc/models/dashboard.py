from odoo import models, fields, api

class BscDashboard(models.Model):
    _name = "bsc.dashboard"

    @api.model
    def get_bsc_data(self):
        bsc = self.env['bsc.bsc'].search([('active','=',True)])
        data = []
        for d in bsc:
            data.append({
                'id': d.id,
                'name': d.name,
                'category': d.category,
                'objectives': [{
                    'id': obj.id,
                    'name': obj.title,
                    'owner': obj.owner.name
                }for obj in d.objective_bsc_ids],
                'measure': [{
                    'id': m.id,
                    'title': m.title,
                    'owner': m.owner.name
                } for m in d.measure_bsc_ids],
                'initiative': [{
                    'id': i.id,
                    'title': i.title,
                    'owner': i.owner.name,
                    'percent_complete': i.percent_complete
                } for i in d.initiative_bsc_ids]
            })
        return data