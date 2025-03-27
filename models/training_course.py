# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, fields, models


class Course(models.Model):
    _name = "training.course"
    _description = "Training course"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    session_ids = fields.One2many("training.session", "course_id", string="Sessions")
    instructor_ids = fields.Many2many("res.users", "training_course_user_rel",
                                      "course_id", "instructor_id")
    duration = fields.Integer("Duration")
    category = fields.Selection(string="Course Category")
    certification_required = fields.Boolean(string="Need certification?")
    renewal_period = fields.Integer("Renewal Period (Days)", required=True)
    expiry_date = fields.Datetime("Expiry Date", compute="calculate_expiry_date", store=True)

    @api.depends('renewal_period')
    def calculate_expiry_date(self):
        for course in self:
            if course.expiry_date and course.renewal_period:
                course.expiry_date = timedelta(days=course.renewal_period)