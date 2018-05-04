# -*- coding: utf-8 -*-
# Part of BSC. See LICENSE file for full copyright and licensing details.
"""
The main duty of this module is to create BSC View getting data
from bsc.bsc. Data will be searched customizing the condition.
Condition is: get data from bsc.bsc, bsc.objective, bsc.measure
and bsc.initiative keeping the relation as it is.
"""
from odoo import models, fields, api

# ------------------------------
# BSC Dashmoard class to search 
# record
# ------------------------------

class BscDashboard(models.Model):
    _name = "bsc.dashboard"

    @api.model
    def get_bsc_data(self):
        """
        fetch data from bsc_bsc and related model
        using relational field. Append data in data
        list which is returned at last.
        """
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