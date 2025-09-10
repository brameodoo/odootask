# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import ValidationError
import re

# 1. Herencia para validar el teléfono y celular en los contactos (res.partner)
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone', 'mobile')
    def _check_phone_and_mobile(self):
        """
        Valida que los campos de teléfono y celular tengan un formato correcto.
        Permite solo números y caracteres comunes de teléfono (+- ()), con un mínimo de 10 dígitos.
        """
        # Regex que permite un '+' opcional, seguido de al menos 10 caracteres válidos.
        phone_regex = re.compile(r"^(?:\+?[\d\s()-]{10,})$")
        
        for partner in self:
            # Validamos el campo de teléfono
            if partner.phone and not phone_regex.match(partner.phone.strip()):
                raise ValidationError(_(
                    "El número de teléfono '%s' no es válido. Debe contener al menos 10 dígitos y solo números o los caracteres (+-).") 
                    % partner.phone
                )
            
            # Validamos el campo de celular
            if partner.mobile and not phone_regex.match(partner.mobile.strip()):
                raise ValidationError(_(
                    "El número de celular '%s' no es válido. Debe contener al menos 10 dígitos y solo números o los caracteres (+-).") 
                    % partner.mobile
                )

# ------------------------------------------------------------------------------------

# 2. Herencia para validar el correo de trabajo en los empleados (hr.employee)
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.constrains('work_email')
    def _check_work_email(self):
        """
        Valida que el correo electrónico del trabajo tenga un formato estándar.
        """
        if self.work_email:
            # Regex estándar y muy confiable (RFC 5322) para validar la mayoría de los correos.
            email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
            
            if not email_regex.match(self.work_email):
                raise ValidationError(_(
                    "La dirección de correo de trabajo '%s' no tiene un formato válido.") 
                    % self.work_email
                )