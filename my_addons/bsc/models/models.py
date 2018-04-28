# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Bsc(models.Model):
	_name = 'bsc.bsc'
	_rec_name = 'name'

	CATEGORY_SELECTION = [
		('financial','Financial'),
		('customer','Customer'),
		('internal','Internal'),
		('learning','Learning'),
	]

	name = fields.Char("Name", required=True)
	company_id = fields.Many2one('res.partner',"Company Name")
	category = fields.Selection(CATEGORY_SELECTION, string="Category", default='financial')
	objective_bsc_ids = fields.One2many('bsc.objective','objective_bsc_ids')

class Objective(models.Model):
	_name = 'bsc.objective'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	# @api.model
    # def _default_collaborator(self):
    #     """ When active_model is res.users, the current partners should be attendees """
    #     partners = self.env.user.partner_id
    #     active_id = self._context.get('active_id')
    #     if self._context.get('active_model') == 'res.users' and active_id:
    #         if active_id not in partners.ids:
    #             partners |= self.env['res.users'].browse(active_id)
    #     return partners

	# filter_user = """
    #             RIGHT JOIN calendar_event_res_partner_rel AS part_rel ON part_rel.calendar_event_id = cal.id
    #                 AND part_rel.res_partner_id = %s
    #     """

	title = fields.Char("Title", required=True)
	owner = fields.Many2one('res.users',
		string= "Owner",
		default=lambda self: self.env.uid)
	objective_bsc_ids = fields.Many2one('bsc.bsc',"BSC")
	# recommendation_objective_ids = fields.One2many('bsc.recommendation','recommendation_objective_ids')
	analysis = fields.Text("Analysis")
	description = fields.Text("Description")
	collaborator_ids = fields.Many2many('res.users', string="Collaborators")
	measure_objective_ids = fields.One2many('bsc.measure','measure_objective_ids')

class Measure(models.Model):
	_name = 'bsc.measure'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	title = fields.Char("Title", required=True)
	analysis = fields.Text("Analysis")
	# recommendation_measure_ids = fields.One2many('bsc.recommendation','recommendation_measure_ids')
	measure_data_measure_ids = fields.One2many('bsc.measuredata','measure_data_measure_ids')
	initiative_measure_ids = fields.One2many('bsc.initiative','measure_id')
	owner = fields.Many2one('res.users',
		string= "Owner",
		default=lambda self: self.env.uid)
	collaborator_ids = fields.Many2many('res.users', string="Collaborators")
	description = fields.Text("Description")
	measure_objective_ids = fields.Many2one('bsc.objective',"Objective")

class Initiative(models.Model):
	_name = 'bsc.initiative'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	title = fields.Char("Title", required=True)
	measure_id = fields.Many2one('bsc.measure',"Measure")
	owner = fields.Many2one('res.users',
		string= "Owner",
		default=lambda self: self.env.uid)
	collaborator_ids = fields.Many2many('res.users','bsc_initiative_res_users_rel', string="Collaborators")
	budget = fields.Float("Budget")
	description = fields.Text("Description")
	percent_complete = fields.Float("Percent Complete")
	analysis = fields.Text("Analysis")
	# recommendation_initiative_ids = fields.One2many('bsc.recommendation','recommendation_initiative_ids')
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	complete_status = fields.Boolean("Complete Status")
	completed_date = fields.Date("Completed Date")
	milestone_initiative_ids = fields.One2many('bsc.milestone','milestone_initiative_ids')
	action_initiative_ids = fields.One2many('bsc.action','action_initiative_ids')

# class Recommendation(models.Model):
# 	_name = 'bsc.recommendation'
# 	_rec_name = 'text'

# 	text = fields.Text("Text")
# 	posted_by = fields.Many2one('res.users',"Posted By")
# 	recommendation_objective_ids = fields.Many2one('bsc.objective',"Recommendations")
# 	recommendation_measure_ids = fields.Many2one('bsc.measure',"Recommendation")
# 	recommendation_initiative_ids = fields.Many2one('bsc.initiative',"Recommendation")

class MeasureData(models.Model):
	_name = 'bsc.measuredata'
	_rec_name = 'measure_data_measure_ids'

	measure_data_measure_ids = fields.Many2one('bsc.measure',"Measure", required=True)
	period = fields.Date("Period")
	actual = fields.Float("Actual")
	target = fields.Float("Target")
	variance = fields.Float("Variance", compute='_get_variance')

	def _get_variance(self):
		for val in self:
			val.variance =  (val.actual - val.target)/abs(val.target)*100

class Milestone(models.Model):
	_name = 'bsc.milestone'
	_rec_name = 'title'

	title = fields.Char("Title", required=True)
	milestone_initiative_ids = fields.Many2one('bsc.initiative',"Initiative")
	owner = fields.Many2one('res.users',
		string= "Owner",
		default=lambda self: self.env.uid)
	percent_complete = fields.Float("Percent Complete")
	analysis = fields.Text("Analysis")
	recommendation = fields.Text("Recommendation")
	collaborator_ids = fields.Many2many('res.users','bsc_milestone_res_users_rel', string="Collaborators")
	description = fields.Text("Description")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	completed_status = fields.Boolean("Completed Status")
	completed_date = fields.Date("Completed Date")
	action_milestone_ids = fields.One2many('bsc.action','action_milestone_ids')

	parent_milestone = fields.Many2one('bsc.milestone',"Milestone")
	child_milestone = fields.One2many('bsc.milestone','parent_milestone')

class Action(models.Model):
	_name = 'bsc.action'
	_rec_name = 'name'

	name = fields.Char("Name", required=True)
	action_initiative_ids = fields.Many2one('bsc.initiative',"Initiative Action")
	action_milestone_ids = fields.Many2one('bsc.milestone',"Milestone Action")
	owner = fields.Many2one('res.users',
		string= "Owner",
		default=lambda self: self.env.uid)
	collaborator_ids = fields.Many2many('res.users','bsc_action_res_users_rel', string="Collaborators")
	description = fields.Text("Description")
	comment = fields.Text("Comment")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	completed_status = fields.Boolean("Completed Status")
	completed_date = fields.Date("Completed Date")