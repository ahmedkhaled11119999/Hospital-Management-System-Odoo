from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date


class Patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'
    _sql_constraints = [
        ('email_unique_constraint', 'UNIQUE(email)', 'This email already exists')
    ]

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    CR_ratio = fields.Float()
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_calc_patient_age')
    department_id = fields.Many2one(comodel_name="hms.department")
    logs_history = fields.One2many(comodel_name="hms.logs", inverse_name="patient_id")
    capacity = fields.Integer(related="department_id.capacity")
    doctors = fields.Many2many("hms.doctor")
    state = fields.Selection([('undetermined', 'Undetermined'),
                              ('good', 'Good'),
                              ('fair', 'Fair'),
                              ('serious', 'Serious')], default='undetermined')

    @classmethod
    def match_regex(cls, user_input, pattern):
        if re.fullmatch(pattern, user_input):
            return True
        else:
            return False

    @api.model
    def create(self, vals_list):
        record = super().create(vals_list)
        self.env['hms.logs'].create({
            'description': 'Created Patient',
            'patient_id': record.id
        })
        return record

    @api.constrains('email')
    def _check_email(self):
        if self.email:
            if not self.match_regex(str(self.email), r"[a-zA-z0-9]+@[a-zA-z]+\.[a-zA-Z]+"):
                raise ValidationError("Please Enter a Valid Email.")

    @api.onchange('birth_date')
    def _on_birth_date_change(self):
        if self.birth_date:
            self.age = date.today().year - self.birth_date.year
        else:
            self.birth_date = '2022-01-01'


    @api.onchange('age')
    def _on_age_change(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Age Changing Alert',
                    'message': 'Age has been changed and is lower than 30, PCR will be checked automatically'
                }
            }

    def set_state_good(self):
        self.state = 'good'
        self.env['hms.logs'].create({
            'description': 'State changed to {}'.format(self.state),
            'patient_id': self.id
        })

    def set_state_fair(self):
        self.state = 'fair'
        self.env['hms.logs'].create({
            'description': 'State changed to {}'.format(self.state),
            'patient_id': self.id
        })

    def set_state_serious(self):
        self.state = 'serious'
        self.env['hms.logs'].create({
            'description': 'State changed to {}'.format(self.state),
            'patient_id': self.id
        })

    def _calc_patient_age(self):
        for rec in self:
            rec.age = date.today().year - rec.birth_date.year





