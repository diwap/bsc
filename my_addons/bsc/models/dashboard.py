from odoo import models, fields, api

class BscDashboard(models.Model):
    _name = "bsc.dashboard"

    def get_bsc_data(self):
        bsc = self.env['bsc.bsc'].search([('name','=','hhhhhhhh')])
        data = []
        objectives = []
        for rec in bsc:
            for re in rec.objective_bsc_ids:
                objectives.append({
                    'name': re.title,
                    'owner': re.owner.name
                })
        for d in bsc:
            data.append({
                'name': d.name,
                'category': d.category,
                'objectives': objectives
            })
        print (data)
        return data