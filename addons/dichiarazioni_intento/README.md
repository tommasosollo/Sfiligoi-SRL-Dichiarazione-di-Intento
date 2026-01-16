# Gestione Dichiarazioni d'Intento

Modulo Odoo per la gestione delle dichiarazioni d'intento dei fornitori.

## Caratteristiche

- **Modello Dichiarazione d'Intento**: Gestione completa di dichiarazioni con codice, date di validità, plafond
- **Integrazione Purchase Order**: Collegamento automatico di dichiarazioni agli ordini di acquisto
- **Validazione Automatica**: Ricerca e applicazione automatica delle dichiarazioni valide per fornitore
- **Report Personalizzato**: Report degli ordini di acquisto con visualizzazione dichiarazione intento e note fiscali

## Funzionalità Principali

### 1. Gestione Dichiarazioni
- Creazione e gestione dichiarazioni d'intento per fornitore
- Codice univoco per fornitore
- Date di validità (inizio/fine)
- Plafond massimo autorizzato
- Note aggiuntive

### 2. Integrazione con Ordini d'Acquisto
- Collegamento automatico della dichiarazione intento al cambio fornitore
- Collegamento manuale via campo specifico
- Snapshot di codice e data della dichiarazione all'applicazione

### 3. Report
Il report dell'ordine di acquisto mostra:
- Etichetta tasse (invoice_label) invece di tax_label
- Codice e data della dichiarazione intento (se collegata)
- Note della posizione fiscale "Dichiarazione di Intento" (se presente)
- Riga "Taxes: 0%" per ordini con dichiarazione intento

## Note Tecniche

### Posizioni Fiscali e Tasse
Per visualizzare le note nel report, la posizione fiscale deve:
- Essere collegata all'ordine
- Avere nome "Dichiarazione di Intento" o "Dichiarazione d'Intento"
- Avere note compilate nel campo "Note"

## Requisiti

- Odoo 19.0
- Moduli dipendenti: base, purchase, account

## Autore

B2T S.R.L.
