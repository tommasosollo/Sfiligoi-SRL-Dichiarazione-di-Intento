# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class DichiarazioneIntento(models.Model):
    """
    Modello per la gestione delle dichiarazioni d'intento fornitori.
    Una dichiarazione d'intento permette di effettuare acquisti con tassazione 0%.
    """
    _name = 'dichiarazione.intento'
    _description = 'Dichiarazione di Intento'
    _rec_name = 'code'
    _order = 'date_start desc, id desc'
    
    _code_uniq = models.Constraint(
        'UNIQUE(code, partner_id)',
        'Il codice della dichiarazione deve essere univoco per fornitore!'
    )

    # Fornitore a cui è associata la dichiarazione
    partner_id = fields.Many2one(
        'res.partner', 
        string='Fornitore', 
        required=True, 
        # domain=[('supplier_rank', '>', 0)],
        help="Seleziona il fornitore per questa dichiarazione"
    )
    # Codice univoco della dichiarazione per fornitore
    code = fields.Char(string='Codice Dichiarazione', required=True)
    # Data della dichiarazione
    declaration_date = fields.Date(string='Data Dichiarazione', required=True)
    # Data inizio validità della dichiarazione
    date_start = fields.Date(string='Data Inizio Validità', required=True)
    # Data fine validità della dichiarazione
    date_end = fields.Date(string='Data Fine Validità', required=True)
    # Anno di riferimento della dichiarazione
    reference_year = fields.Integer(string='Anno di Riferimento', required=True, default=lambda self: datetime.now().year, aggregator=None)
    # Importo massimo autorizzato dalla dichiarazione
    plafond = fields.Float(string='Plafond', required=True, digits=(16, 2))
    # Stato della dichiarazione (attiva o disattivata)
    active = fields.Boolean(string='Attiva', default=True)
    # Note aggiuntive sulla dichiarazione
    note = fields.Text(string='Note')
    
    # Ammontare IVA degli ordini collegati (calcolato automaticamente)
    total_amount = fields.Float(string='Ammontare IVA Ordini (simulata)', compute='_compute_total_amount', digits=(16, 2), store=True)
    # Relazione inversa con gli ordini di acquisto
    purchase_order_ids = fields.One2many('purchase.order', 'dichiarazione_intento_id', string='Ordini d\'Acquisto', readonly=True)
    
    @api.depends('purchase_order_ids', 'purchase_order_ids.amount_total')
    def _compute_total_amount(self):
        """
        Calcola l'ammontare totale e l'IVA simulata di tutti gli ordini di acquisto collegati a questa dichiarazione.
        """
        for declaration in self:
            total = sum(order.amount_total for order in declaration.purchase_order_ids)
            declaration.total_amount = 0.22 * total

    def write(self, vals):
        res = super(DichiarazioneIntento, self).write(vals)
        
        # Se stiamo disattivando (vals contiene 'active': False)
        if 'active' in vals and not vals['active']:
            # Inviamo la notifica tramite il BUS di Odoo
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,  # Destinatario (l'utente attuale)
                'simple_notification',     # Tipo di evento ascoltato dal client web
                {
                    'type': 'warning',     # 'warning', 'danger', 'info', 'success'
                    'title': "Promemoria",
                    'message': "Hai disattivato la dichiarazione. Ricordati di aggiornare la posizione fiscale del fornitore!",
                    'sticky': True,        # True = Rimane finché non la chiudi con la X
                }
            )
            
        return res