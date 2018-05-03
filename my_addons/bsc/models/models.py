# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime

STATES = [
    ('initial', 'Initial'),
    ('completed', 'Completed'),
	('missed', 'Deadline Missed')
]

class Person:
	def __init__(self, d1, d2):
		self.d1 = d1
		self.d2 = d2

	def check_date(self):
		if self.d1 and self.d2:
			if self.d1 > self.d2:
				raise ValidationError("Your start date is greater than end date. \nStart Date: %s \nEnd Date: %s"%(self.d1, self.d2))

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

	color = fields.Integer(string='Color Index', help="The color of the channel")
	obj_count = fields.Integer("Count Objectives", compute="_objectives_count")
	meas_count = fields.Integer("Count Measure", compute="_measures_count")
	init_count = fields.Integer("Count Initiatives", compute="_initiatives_count")

	_sql_constraints = [
		('name_uniq', 'unique(name)', 'BSC name must be unique'),
	]

	def _objectives_count(self):
		for rec in self:
			rec.obj_count = rec.env['bsc.objective'].search_count([('objective_bsc_ids.name', '=', rec.name)])
	
	def _measures_count(self):
		for rec in self:
			rec.meas_count = rec.env['bsc.measure'].search_count([('measure_objective_ids.objective_bsc_ids.name', '=', rec.name)])

	def _initiatives_count(self):
		for rec in self:
			rec.init_count = rec.env['bsc.initiative'].search_count([('measure_id.measure_objective_ids.objective_bsc_ids.name', '=', rec.name)])

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
	percent_complete = fields.Float("Percent Complete", compute="_get_percent_complete")
	analysis = fields.Text("Analysis")
	# recommendation_initiative_ids = fields.One2many('bsc.recommendation','recommendation_initiative_ids')
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	complete_status = fields.Boolean("Complete Status")
	completed_date = fields.Date("Completed Date", compute="_get_completed_date")
	milestone_initiative_ids = fields.One2many('bsc.milestone','milestone_initiative_ids')
	# action_initiative_ids = fields.One2many('bsc.action','action_initiative_ids')

	state = fields.Selection(STATES, string='Completed Status', default='initial', readonly=True, index=True)

	def _get_percent_complete(self):
		for rec in self:
			try:
				completed = []
				for ms in rec.milestone_initiative_ids:
					if ms.completed_status == True:
						completed.append(ms.milestone_initiative_ids)
				rec.percent_complete = len(completed)/len(rec.milestone_initiative_ids)*100
			except ZeroDivisionError:
				rec.percent_complete = 0

	@api.onchange('end_date')
	def _check_date(self):
		for rec in self:
			ndate = Person(rec.start_date, rec.end_date)
			return ndate.check_date()

	def _get_completed_date(self):
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_date = date.today()
			if rec.end_date and rec.completed_date:
				if rec.end_date < rec.completed_date:
					rec.write({'state': 'missed'})
				else:
					rec.write({'state': 'completed'})

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
	percent_complete = fields.Float("Percent Complete", compute='_get_percent_complete')
	analysis = fields.Text("Analysis")
	recommendation = fields.Text("Recommendation")
	collaborator_ids = fields.Many2many('res.users','bsc_milestone_res_users_rel', string="Collaborators")
	description = fields.Text("Description")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date", compute="_get_end_date")
	completed_status = fields.Boolean("Completed Status", compute="_get_completed_status")
	completed_date = fields.Date("Completed Date", compute="_get_completed_date")
	action_milestone_ids = fields.One2many('bsc.action','action_milestone_ids')

	parent_milestone = fields.Many2one('bsc.milestone',"Milestone")
	child_milestone = fields.One2many('bsc.milestone','parent_milestone')
	state = fields.Selection(STATES, string='Completed Status', default='initial', readonly=True, index=True)

	def _get_percent_complete(self):
		for rec in self:
			try:
				completed = []
				for ms in rec.action_milestone_ids:
					if ms.completed_status == True:
						completed.append(ms.action_milestone_ids)
				rec.percent_complete = len(completed)/len(rec.action_milestone_ids)*100
			except ZeroDivisionError:
				rec.percent_complete = 0

	def _get_completed_date(self):
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_date = date.today()
			if rec.end_date and rec.completed_date:
				if rec.end_date < rec.completed_date:
					rec.write({'state': 'missed'})
				else:
					rec.write({'state': 'completed'})
	
	def _get_completed_status(self):
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_status = True

	def _get_end_date(self):
		for rec in self:
			max_time = []
			for dt in rec.action_milestone_ids:
				max_time.append(datetime.strptime(dt.end_date, '%Y-%m-%d').date())
			if max_time:
				rec.end_date = max(max_time)

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
	completed_status = fields.Boolean("Completed Status", readonly=True)
	completed_date = fields.Date("Completed Date")
	state = fields.Selection(STATES, string='Completed Status', default='initial', readonly=True, index=True)

	@api.onchange('end_date')
	def _check_date(self):
		for rec in self:
			ndate = Person(rec.start_date, rec.end_date)
			return ndate.check_date()

	def toggle_status(self):
		for rec in self:
			rec.completed_date = date.today()
			if rec.completed_status == False:
				rec.completed_status = True
		if self.end_date < self.completed_date:
			rec.write({'state': 'missed'})
		else:
			rec.write({'state': 'completed'})
		return True

	def reset_complete(self):
		for rec in self:
			if rec.completed_status == True:
				rec.completed_date = None
				rec.completed_status = False
		return rec.write({'state': 'initial'})