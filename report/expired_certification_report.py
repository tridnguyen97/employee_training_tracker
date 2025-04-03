# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExpiredCertificationReport(models.AbstractModel):
    _name = 'report.employee_training_tracker.report_expired_certifications'
    _description = 'Expired Certifications Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = fields.Datetime.now()
        expired_completions = self.env['training.completion'].search([
            ('expiry_date', '<', today),
            ('expiry_date', '!=', False), #To filter out training that do not expire.
        ])

        return {
            'expired_completions': expired_completions,
        }
