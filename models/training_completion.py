# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, models, fields

class Completion(models.Model):
    _name = "training.completion"
    _description = "Training Completion"

    employee_id = fields.Many2one("res.users", string="Employee")
    course_id = fields.Many2one("training.course", string="Course")
    completion_date = fields.Date("Completion Date")
    expiry_date = fields.DateTime("Expiry Date", compute="_compute_expiry_date")

    _sql_constraints = [
        ('unique_course_attendee', 'unique(course_id, attendee_id)',
         'An attendee can only have one completion record per course.'),
    ]

    @api.depends("course_id", "course_id.renewal_period")
    def _compute_expiry_date(self):
        for completion in self:
            if completion.course_id:
                if completion.course_id.renewal_period and \
                  completion.course_id.certification_required:
                    completion.expiry_date += timedelta()