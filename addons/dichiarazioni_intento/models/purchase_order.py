# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
    
    def write(self, vals):
        """
        Metodo di salvataggio dell'ordine.
        Se l'ordine ha una dichiarazione d'intento collegata, azzera le tasse su tutte le righe.
        """
        result = super().write(vals)
        for order in self:
            if order.dichiarazione_intento_id:
                # Se c'è una dichiarazione d'intento, azzera le tasse su tutte le righe
                for line in order.order_line:
                    line.tax_ids = False
        return result

    @api.onchange('partner_id')
    def _onchange_dichiarazione_intento_auto_apply(self):
        """
        Metodo automatico che ricerca una dichiarazione d'intento valida quando cambia il fornitore.
        Criteri di ricerca:
        1. Fornitore corrisponde
        2. Dichiarazione attiva
        Ricerca la prima dichiarazione che corrisponde ai criteri.
        """
        if not self.partner_id:
            # Se non c'è un fornitore selezionato, cancella i campi della dichiarazione
            self.dichiarazione_intento_id = False
            self.dichiarazione_intento_code = False
            self.dichiarazione_intento_date = False
            return

        # Costruisce il filtro di ricerca per la dichiarazione valida
        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('active', '=', True),
        ]
        
        # Ricerca la prima dichiarazione che corrisponde ai criteri
        declaration = self.env['dichiarazione.intento'].search(domain, limit=1)

        if declaration:
            # Se trovata, la applica all'ordine
            self.dichiarazione_intento_id = declaration.id
            self.dichiarazione_intento_code = declaration.code
            self.dichiarazione_intento_date = declaration.declaration_date
            if declaration.fiscal_position_id:
                # Applica la posizione fiscale della dichiarazione
                self.fiscal_position_id = declaration.fiscal_position_id
                self._recompute_taxes()
        else:
            # Se non trovata, cancella i dati della dichiarazione
            self.dichiarazione_intento_id = False
            self.dichiarazione_intento_code = False
            self.dichiarazione_intento_date = False

    @api.onchange('dichiarazione_intento_id')
    def _onchange_dichiarazione_intento_id(self):
        """
        Metodo che si attiva quando l'utente seleziona manualmente una dichiarazione d'intento.
        Aggiorna i campi snapshot e applica la posizione fiscale.
        """
        if self.dichiarazione_intento_id:
            # Aggiorna i campi snapshot
            self.dichiarazione_intento_code = self.dichiarazione_intento_id.code
            self.dichiarazione_intento_date = self.dichiarazione_intento_id.declaration_date
            if self.dichiarazione_intento_id.fiscal_position_id:
                # Applica la posizione fiscale e ricalcola le tasse
                self.fiscal_position_id = self.dichiarazione_intento_id.fiscal_position_id
                self._recompute_taxes()
    
    def _recompute_taxes(self):
        """
        Ricalcola le tasse su tutte le righe dell'ordine.
        Se c'è una dichiarazione d'intento, azzera le tasse.
        Altrimenti applica la posizione fiscale dell'ordine.
        """
        for line in self.order_line:
            if self.dichiarazione_intento_id:
                # Con dichiarazione d'intento, le tasse sono azzerate a 0%
                line.tax_ids = False
            elif self.fiscal_position_id and line.product_id:
                # Altrimenti applica la mappatura della posizione fiscale
                taxes = line.product_id.supplier_taxes_id
                line.tax_ids = self.fiscal_position_id.map_tax(taxes)
