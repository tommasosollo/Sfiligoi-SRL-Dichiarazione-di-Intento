# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    """
    Estensione del modello Partner per visualizzare le dichiarazioni d'intento associate.
    """
    _inherit = 'res.partner'

    # Relazione inversa con le dichiarazioni d'intento del partner (fornitore)
    dichiarazione_intento_ids = fields.One2many(
        'dichiarazione.intento', 
        'partner_id', 
        string='Dichiarazioni d\'Intento'
    )
