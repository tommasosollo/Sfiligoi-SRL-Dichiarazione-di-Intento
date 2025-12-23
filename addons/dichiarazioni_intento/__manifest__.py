# -*- coding: utf-8 -*-
"""
Manifest del modulo per la gestione delle dichiarazioni d'intento.
Configura le proprietà, le dipendenze e i file di dati del modulo.
"""
{
    'name': "Gestione Dichiarazioni d'Intento",
    'summary': "Gestione delle dichiarazioni d'intento fornitori",
    'description': """
        Modulo per la gestione delle dichiarazioni d'intento dei fornitori.
        Caratteristiche principali:
        - Modello dedicato per le dichiarazioni
        - Integrazione con res.partner
        - Applicazione automatica su purchase.order
        - Gestione validità e plafond
    """,
    'author': "Tommaso Sollo",
    'website': "https://www.tommasosollo.it",
    'category': 'Purchase',
    'version': '19.0.1.0.0',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/dichiarazione_intento_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
        'views/menus.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
