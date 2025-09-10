import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = "hr.employee"  # 🔹 Heredamos el modelo de empleados

    @api.constrains("l10n_mx_curp")
    def _check_curp(self):
        """
        Valida que el formato de la CURP sea correcto utilizando una expresión regular robusta.
        """
        # Regex mejorado que valida la estructura interna de la CURP (fecha, estado, consonantes).
        curp_regex = r"^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$"
        for record in self:
            if record.l10n_mx_curp and not re.match(curp_regex, record.l10n_mx_curp):
                raise ValidationError("La CURP ingresada no tiene un formato válido. Por favor, verifícala.")

    @api.constrains("l10n_mx_rfc")  # Cambiado de "rfc" a "l10n_mx_rfc"
    def _check_rfc(self):
        """
        Valida que el formato del RFC sea correcto, aceptando personas físicas y morales.
        """
        rfc_regex = r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$"
        for record in self:
            # La validación solo se ejecuta si el campo tiene un valor.
            # Se cambió 'record.rfc' por 'record.l10n_mx_rfc' en todas las líneas.
            if record.l10n_mx_rfc and not re.match(rfc_regex, record.l10n_mx_rfc.upper()):
                raise ValidationError(_(
                    "El RFC '%s' no tiene un formato válido. Debe tener 12 (persona moral) o 13 (persona física) caracteres y cumplir con el formato oficial.")
                    % record.l10n_mx_rfc
                )


