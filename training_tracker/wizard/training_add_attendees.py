# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrainingAddAttendees(models.TransientModel):
    _name = "training.add.attendees"

    session_id = fields.Many2one("training.session", string="Session",
                                 required=True)
    attendees_ids = fields.Many2many("res.users", "add_attendees_users_rel",
                                     "added_id", "attendee_id")

    def action_add_attendees_and_create_completion(self):
        # ensure only 1 record to handle
        self.ensure_one()
        if self.session_id and self.attendees_ids:
            # add selected attendees in the wizard
            self.session_id.attendee_ids |= self.attendees_ids
            for attendee in self.attendees_ids:
                # create a new completion record
                self.env["training.completion"].create({
                    "course_id": self.session_id.course_id.id,
                    "attendee_id": attendee.id,
                    "completion_date": fields.Date.today()
                })
        return {"type": "ir.actions.act_window.window_close"}
