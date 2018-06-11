# -*- coding: utf-8 -*-
# Part of BSC. See LICENSE file for full copyright and licensing details.

"""
The main duty of this module is to create ORM with controller
for BSC View. In BSC view we have relation with objective,
measure and initiatives. Bsc view can be either archived or
unarchived.

Objective and Measure are more of a similar nature in code
perspective. Measure has relation with measure data. Initiative
has time constraints. It has relation with milestone.

Milestone depends on action. The properties of milestone is more
dependent on action.
"""
from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

STATES = [
	('initial', 'Initial'),
	('completed', 'Completed'),
	('missed', 'Deadline Missed')
]

# --------------------------------------------------------
# Check two date and raise validation error if first date
# is greater than second date. To use this function first
# create new instance of class and pass argument. Secondly
# call method.
# --------------------------------------------------------


class CheckDate:
	def __init__(self, d1, d2):
		self.d1 = d1
		self.d2 = d2

	def check_date(self):
		if self.d1 and self.d2:
			if self.d1 > self.d2:
				raise ValidationError(
					"Your start date is greater than end date.\n
					Start Date: % s \n
					End Date: % s
					" % (self.d1, self.d2)
				)

# ----------------------------
# Balance Scorecard main model
# ----------------------------


class Bsc(models.Model):
	_name = 'bsc.bsc'
	_rec_name = 'name'

	CATEGORY_SELECTION = [
		('financial', 'Financial'),
		('customer', 'Customer'),
		('internal', 'Internal'),
		('learning', 'Learning'),
	]

	# Main ORM
	name = fields.Char("Name", required=True)
	company_id = fields.Many2one('res.partner', "Company Name")
	category = fields.Selection(
		CATEGORY_SELECTION,
		string="Category",
		default='financial'
	)
	objective_bsc_ids = fields.One2many('bsc.objective', 'objective_bsc_ids')
	measure_bsc_ids = fields.One2many('bsc.measure', 'measure_bsc_ids')
	initiative_bsc_ids = fields.One2many('bsc.initiative', 'initiative_bsc_ids')

	# ORM for functionality
	color = fields.Integer(string='Color Index', help="The color of the channel")
	obj_count = fields.Integer("Count Objectives", compute="_objectives_count")
	meas_count = fields.Integer("Count Measure", compute="_measures_count")
	init_count = fields.Integer("Count Initiatives", compute="_initiatives_count")
	active = fields.Boolean(default=True)

	# make every name of a record unique
	_sql_constraints = [
		('name_uniq', 'unique(name)', 'BSC name must be unique'),
	]

	def _objectives_count(self):
		""" Count number of objective in a BSC. """
		for rec in self:
			rec.obj_count = rec.env['bsc.objective'].search_count([
				('objective_bsc_ids.name', '=', rec.name)
			])

	def _measures_count(self):
		""" Count number of measure in BSC. """
		for rec in self:
			rec.meas_count = rec.env['bsc.measure'].search_count([
				('measure_bsc_ids.name', '=', rec.name)
			])

	def _initiatives_count(self):
		""" Count number of initiative in BSC. """
		for rec in self:
			rec.init_count = rec.env['bsc.initiative'].search_count([
				('initiative_bsc_ids.name', '=', rec.name)
			])

# ---------------------------
# Objective Model
# ---------------------------


class Objective(models.Model):
	_name = 'bsc.objective'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	# Main ORM
	title = fields.Char("Title", required=True, track_visibility='onchange')
	owner = fields.Many2one(
		'res.users',
		string="Owner",
		default=lambda self: self.env.uid
	)  # get current logged in user id
	objective_bsc_ids = fields.Many2one('bsc.bsc', "BSC")
	analysis = fields.Text("Analysis")
	description = fields.Text("Description")
	collaborator_ids = fields.Many2many('res.users', string="Collaborators")

# -------------------------
# Measure Model
# -------------------------


class Measure(models.Model):
	_name = 'bsc.measure'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	# Main ORM
	# Track Visibility onchange is to keep log of changes in footer message
	title = fields.Char("Title", required=True, track_visibility='onchange')
	analysis = fields.Text("Analysis")
	measure_data_measure_ids = fields.One2many(
		'bsc.measuredata',
		'measure_data_measure_ids'
	)
	owner = fields.Many2one(
		'res.users',
		string="Owner",
		default=lambda self: self.env.uid
	)
	collaborator_ids = fields.Many2many('res.users', string="Collaborators")
	description = fields.Text("Description")
	measure_bsc_ids = fields.Many2one('bsc.bsc', "Objective")

# ----------------------------
# Initiative Model
# ----------------------------


class Initiative(models.Model):
	_name = 'bsc.initiative'
	_inherit = 'mail.thread'
	_rec_name = 'title'

	# Main ORM
	title = fields.Char("Title", required=True, track_visibility='onchange')
	initiative_bsc_ids = fields.Many2one('bsc.bsc', "BSC")
	owner = fields.Many2one(
		'res.users',
		string="Owner",
		default=lambda self: self.env.uid)
	collaborator_ids = fields.Many2many(
		'res.users',
		'bsc_initiative_res_users_rel',
		string="Collaborators"
	)
	budget = fields.Float("Budget", track_visibility='onchange')
	description = fields.Text("Description")
	percent_complete = fields.Float(
		"Percent Complete",
		compute="_get_percent_complete",
		track_visibility='always'
	)
	analysis = fields.Text("Analysis")
	start_date = fields.Date("Start Date", track_visibility='onchange')
	end_date = fields.Date("End Date", track_visibility='onchange')
	completed_date = fields.Date("Completed Date", compute="_get_completed_date")
	milestone_initiative_ids = fields.One2many(
		'bsc.milestone',
		'milestone_initiative_ids'
	)

	# Orm for functionality
	complete_status = fields.Boolean("Complete Status")
	state = fields.Selection(
		STATES,
		string='Completed Status',
		default='initial',
		readonly=True,
		index=True
	)

	@api.onchange('budget')
	def _validate_budget(self):
		"""
		Check budget value is less than zero.
		If true, change value to zero
		"""
		for rec in self:
			if rec.budget < 0:
				rec.budget = 0

	def _get_percent_complete(self):
		"""
		Calculate percent_complete getting
		length of total record and length of
		record whose completed_status is True
		"""
		for rec in self:
			try:
				completed = []
				for ms in rec.milestone_initiative_ids:
					if ms.completed_status:
						completed.append(ms.milestone_initiative_ids)
				rec.percent_complete = len(completed)/len(rec.milestone_initiative_ids)*100
			except ZeroDivisionError:
				# If error occur, change value of percent_complete to zero
				rec.percent_complete = 0

	# onchange is used to run function,
	# if any change in given argument occur
	@api.onchange('end_date')
	def _check_date(self):
		for rec in self:
			ndate = CheckDate(rec.start_date, rec.end_date)
			return ndate.check_date()

	def _get_completed_date(self):
		"""
		Update completed_date value if
		percent_complete is 100%. Update
		state based on the situation of end_date
		and completed_date.
		"""
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_date = date.today()
			if rec.end_date and rec.completed_date:
				if rec.end_date < rec.completed_date:
					rec.write({'state': 'missed'})
				else:
					rec.write({'state': 'completed'})


# ----------------------------
# Measure data Model
# ----------------------------

class MeasureData(models.Model):
	_name = 'bsc.measuredata'
	_rec_name = 'measure_data_measure_ids'

	measure_data_measure_ids = fields.Many2one(
		'bsc.measure',
		"Measure",
		required=True
	)
	period = fields.Date("Period")
	actual = fields.Float("Actual")
	target = fields.Float("Target")
	variance = fields.Float("Variance", compute='_get_variance')

	def _get_variance(self):
		"""
		calculate variance getting data from
		actual and target.
		"""
		for val in self:
			try:
				val.variance = (val.actual - val.target)/abs(val.target)*100
			except ZeroDivisionError:
				val.variance = 0

	@api.onchange('target')
	def _validate_price(self):
		"""
		Check target value is less than zero.
		If true, change value to zero
		"""
		for rec in self:
			if rec.target < 0:
				rec.target = 0

# ----------------------------
# Milestone Model
# ----------------------------


class Milestone(models.Model):
	_name = 'bsc.milestone'
	_rec_name = 'title'

	# Main ORM
	title = fields.Char("Title", required=True)
	milestone_initiative_ids = fields.Many2one('bsc.initiative', "Initiative")
	owner = fields.Many2one(
		'res.users',
		string="Owner",
		default=lambda self: self.env.uid
	)
	analysis = fields.Text("Analysis")
	recommendation = fields.Text("Recommendation")
	collaborator_ids = fields.Many2many(
		'res.users',
		'bsc_milestone_res_users_rel',
		string="Collaborators"
	)
	description = fields.Text("Description")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date", compute="_get_end_date")
	completed_date = fields.Date("Completed Date", compute="_get_completed_date")
	action_milestone_ids = fields.One2many('bsc.action', 'action_milestone_ids')

	# ORM for functionality
	completed_status = fields.Boolean(
		"Completed Status",
		compute="_get_completed_status"
	)
	percent_complete = fields.Float(
		"Percent Complete",
		compute='_get_percent_complete'
	)
	parent_milestone = fields.Many2one('bsc.milestone', "Milestone")
	child_milestone = fields.One2many('bsc.milestone', 'parent_milestone')
	state = fields.Selection(
		STATES,
		string='Completed Status',
		default='initial',
		readonly=True,
		index=True
	)

	def _get_percent_complete(self):
		"""
		Calculate percent_complete getting
		length of total record and length of
		record whose completed_status is True
		"""
		for rec in self:
			try:
				completed = []
				for ms in rec.action_milestone_ids:
					if ms.completed_status:
						completed.append(ms.action_milestone_ids)
				rec.percent_complete = len(completed)/len(rec.action_milestone_ids)*100
			except ZeroDivisionError:
				rec.percent_complete = 0

	def _get_completed_date(self):
		"""
		Update completed_date value if
		percent_complete is 100%. Update
		state based on the situation of end_date
		and completed_date.
		"""
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_date = date.today()
			if rec.end_date and rec.completed_date:
				if rec.end_date < rec.completed_date:
					rec.write({'state': 'missed'})
				else:
					rec.write({'state': 'completed'})

	def _get_completed_status(self):
		"""
		Update completed_status value
		if percent_complete is 100%.
		"""
		for rec in self:
			if rec.percent_complete == 100:
				rec.completed_status = True

	def _get_end_date(self):
		"""
		Append all end date of action in max_time list.
		max function is used to get largest date.
		"""
		for rec in self:
			max_time = []
			for dt in rec.action_milestone_ids:
				if not dt:
					# date by default is string so date() function convert it to object
					max_time.append(datetime.strptime(dt.end_date, '%Y-%m-%d').date())
			if max_time:
				rec.end_date = max(max_time)

# ----------------------------
# Action Model
# ----------------------------


class Action(models.Model):
	_name = 'bsc.action'
	_rec_name = 'name' 

	# Main ORM
	name = fields.Char("Name", required=True)
	action_initiative_ids = fields.Many2one('bsc.initiative', "Initiative Action")
	action_milestone_ids = fields.Many2one('bsc.milestone', "Milestone Action")
	owner = fields.Many2one(
		'res.users',
		string="Owner",
		default=lambda self: self.env.uid
	)
	collaborator_ids = fields.Many2many(
		'res.users',
		'bsc_action_res_users_rel',
		string="Collaborators"
	)
	description = fields.Text("Description")
	comment = fields.Text("Comment")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	completed_date = fields.Date("Completed Date")

	# ORM for functionality
	completed_status = fields.Boolean("Completed Status", readonly=True)
	state = fields.Selection(
		STATES,
		string='Completed Status',
		default='initial',
		readonly=True,
		index=True
	)

	@api.onchange('end_date')
	def _check_date(self):
		"""
		Check if date is valid
		"""
		for rec in self:
			ndate = CheckDate(rec.start_date, rec.end_date)
			return ndate.check_date()

	def toggle_status(self):
		"""
		When event is triggered completed status
		is changed to True if False. Update state
		based on the condition of end_date and
		completed_date.
		"""
		for rec in self:
			rec.completed_date = date.today()
			if not rec.completed_status:
				rec.completed_status = True
		if self.end_date:
			if self.end_date < self.completed_date:
				rec.write({'state': 'missed'})
			else:
				rec.write({'state': 'completed'})
		else:
			raise UserError("No End date defined")
		return True

	def reset_complete(self):
		"""
		change completed_status to false and completed_date
		value is removed if completed_status is true. Reset
		state of record to initial
		"""
		for rec in self:
			if rec.completed_status:
				rec.completed_date = None
				rec.completed_status = False
		return rec.write({'state': 'initial'})
