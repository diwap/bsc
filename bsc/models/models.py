# -*- coding: utf-8 -*-

from odoo import models, fields, api

class bsc(models.Model):
	_name = 'bsc.bsc'
	_rec_name = 'name'

	name = fields.Many2one('res.partner',"Name")
