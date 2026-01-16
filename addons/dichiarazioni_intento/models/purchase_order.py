# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class PurchaseOrder(models.Model):
    """
    Estensione del modello Ordine d'Acquisto per l'integrazione con le dichiarazioni d'intento.
    Aggiunge la possibilità di collegare una dichiarazione d'intento a un ordine e azzerare le tasse.
    """
    _inherit = 'purchase.order'

    # Dichiarazione d'intento collegata all'ordine
    dichiarazione_intento_id = fields.Many2one(
        'dichiarazione.intento',
        string='Dichiarazione d\'Intento',
        domain="[('partner_id', '=', partner_id), ('active', '=', True)]",
        help="Dichiarazione d'intento applicata a questo ordine"
    )
    # Codice della dichiarazione (snapshot del valore al momento dell'applicazione)
    dichiarazione_intento_code = fields.Char(string='Codice Dichiarazione (Snapshot)')
    # Data della dichiarazione (snapshot del valore al momento dell'applicazione)
    dichiarazione_intento_date = fields.Date(string='Data Dichiarazione (Snapshot)')
    
    
    @api.onchange('partner_id')
    def _onchange_dichiarazione_intento_auto_apply(self):
        """
        Metodo automatico che ricerca una dichiarazione d'intento valida quando cambia il fornitore.
        Criteri di ricerca:
        1. Fornitore corrisponde
        2. Dichiarazione attiva
        3. Anno di competenza corrisponde all'anno corrente
        Ricerca l'ultima dichiarazione per data inizio validità che corrisponde ai criteri.
        """
        if not self.partner_id:
            # Se non c'è un fornitore selezionato, cancella i campi della dichiarazione
            self.dichiarazione_intento_id = False
            self.dichiarazione_intento_code = False
            self.dichiarazione_intento_date = False
            return

        # Determina l'anno di competenza (anno corrente)
        current_year = datetime.now().year
        
        # Costruisce il filtro di ricerca per la dichiarazione valida
        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('active', '=', True),
            ('reference_year', '=', current_year),
        ]
        
        # Ricerca le dichiarazioni che corrispondono ai criteri, ordinate per data_start descending
        # Prende l'ultima per data inizio validità
        declaration = self.env['dichiarazione.intento'].search(domain, order='date_start desc', limit=1)

        if declaration:
            # Se trovata, la applica all'ordine
            self.dichiarazione_intento_id = declaration.id
            self.dichiarazione_intento_code = declaration.code
            self.dichiarazione_intento_date = declaration.declaration_date
        else:
            # Se non trovata, cancella i dati della dichiarazione
            self.dichiarazione_intento_id = False
            self.dichiarazione_intento_code = False
            self.dichiarazione_intento_date = False

    @api.onchange('dichiarazione_intento_id')
    def _onchange_dichiarazione_intento_id(self):
        """
        Metodo che si attiva quando l'utente seleziona manualmente una dichiarazione d'intento.
        Aggiorna i campi snapshot.
        """
        if self.dichiarazione_intento_id:
            # Aggiorna i campi snapshot
            self.dichiarazione_intento_code = self.dichiarazione_intento_id.code
            self.dichiarazione_intento_date = self.dichiarazione_intento_id.declaration_date