from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Campo técnico para mostrar el número en la ficha
    registration_number = fields.Char(string="Nº de Empleado", copy=False, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('registration_number'):
                # Genera el siguiente (Ej: EMP00098)
                new_seq = self.env['ir.sequence'].next_by_code('hr.employee.number')
                vals['registration_number'] = new_seq
                # El PIN toma solo los números (Ej: 00098)
                vals['pin'] = ''.join(filter(str.isdigit, new_seq))
        return super(HrEmployee, self).create(vals_list)

    def action_generate_numbers_by_seniority(self):
        """
        Ordena a los empleados por su fecha de contrato y asigna 
        los números EMP00001, EMP00002, etc.
        """
        # 1. Buscamos empleados sin número asignado
        employees = self.search([('registration_number', '=', False)])
        
        if not employees:
            raise UserError(_("No hay empleados pendientes de numeración."))

        # 2. Ordenar por fecha de contrato (el campo que acabas de importar)
        # Usamos create_date como respaldo si la fecha de contrato fallara
        sorted_employees = sorted(
            employees, 
            key=lambda e: e.contract_id.date_start if e.contract_id and e.contract_id.date_start else e.create_date
        )

        # 3. Asignación masiva en orden
        for emp in sorted_employees:
            new_seq = self.env['ir.sequence'].next_by_code('hr.employee.number')
            # Extraer solo dígitos para el PIN
            numeric_pin = ''.join(filter(str.isdigit, new_seq))
            
            emp.write({
                'registration_number': new_seq,
                'pin': numeric_pin
            })
        
        return {
            'effect': {
                'fadeout': 'slow',
                'message': '¡Numeración completada con éxito!',
                'type': 'rainbow_man',
            }
        }
