# -*- coding: utf-8 -*-

from odoo import api, fields, exceptions, models
from datetime import timedelta

class Session(models.Model):

    _name = "training.session"
    _description = "Training Session"

    course_id = fields.Many2one("training.course", string="Course")
    start_date = fields.Datetime("Start Date")
    duration = fields.Float("Duration (Hours)")
    end_date = fields.Datetime("End Date", compute="_compute_end_date")
    instructor_id = fields.Many2one("res.users", string="Instructor")
    attendees_ids = fields.Many2many("res.users", "training_session_users_rel",
                                    "training_session_id", "attendee_id")
    total_sessions = fields.Integer(string="Total Sessions", compute='_compute_total_sessions', store=True)

    @api.depends('session_ids')
    def _compute_total_sessions(self):
        for record in self:
            record.total_sessions = len(record.session_ids)

    @api.depends("start_date", "end_date")
    def _compute_end_date(self):
        for session in self:
            if session.start_date and session.duration:
                session.end_date = session.start_date + timedelta(hours=session.duration)
            else:
                session.end_date = False    
    
    def check_session_overlap(self):
        """Validates no overlapping sessions for an instructor."""
        for session in self:
            if not session.instructor_id or not session.start_date or \
              not session.end_date:
                continue
            overlapped_session = self.search([
                ("id", "!=", session.id),
                ("start_date", "<", session.start_date),
                ("end_date", ">", session.end_date),
                ("instructor_id", "=", session.instructor_id.id),
            ])
            if overlapped_session:
                raise exceptions.ValidationError(
                    "This session overlaps with another session "
                    "for the same instructor")
    
    @api.constrains("start_date", "duration", "instructor_id")
    def _check_overlap_constrains(self):
        for session in self:
            session.check_session_overlap()
