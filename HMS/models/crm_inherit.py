from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError


class CrmInherit(models.Model):

    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(comodel_name='hms.patient')

    @api.constrains('related_patient_id')
    def _patient_email_validate(self):
        if self.email == self.related_patient_id.email:
            raise ValidationError("You can't choose a patient that has the same email.")

    def unlink(self):
        if self.related_patient_id:
            raise UserError("Can't delete Customer because it is linked to a patient.")
        return super().unlink()

