from odoo import models, fields, api

class BscDashboard(models.Model):
    _name = "bsc.dashboard"

    @api.model
    def get_bsc_data(self):
        bsc = self.env['bsc.bsc'].search([('active','=',True)])
        data = []
        # objectives = []
        # measure = []
        # initiative = []
        # for rec in bsc:
        #     for re in rec.objective_bsc_ids:
        #         objectives.append({
        #             'name': re.title,
        #             'owner': re.owner.name
        #         })
        # for rec in bsc:
        #     for m in bsc.measure_bsc_ids:
        #         measure.append({
        #             'title': m.title,
        #             'owner': m.owner.name
        #         })
        # for rec in bsc:
        #     for i in bsc.initiative_bsc_ids:
        #         initiative.append({
        #             'title': i.title,
        #             'owner': i.owner.name
        #         })
        for d in bsc:
            data.append({
                'name': d.name,
                'category': d.category,
                'objectives': [{
                    'name': obj.title,
                    'owner': obj.owner.name
                }for obj in d.objective_bsc_ids],
                'measure': [{
                    'title': m.title,
                    'owner': m.owner.name
                } for m in d.measure_bsc_ids],
                'initiative': [{
                    'title': i.title,
                    'owner': i.owner.name
                } for i in d.initiative_bsc_ids]
            })
        # ser_rec = self.env['bsc.bsc'].search_read([])
        # print (ser_rec)
        # print ("\n\n\n\n\n\n\n")
        # print (ser_rec)
        # print ("\n\n\n\n\n\n\n")
        # print (", ".join( repr(e) for e in data ))
        # return (", ".join( repr(e) for e in data ))
        return data