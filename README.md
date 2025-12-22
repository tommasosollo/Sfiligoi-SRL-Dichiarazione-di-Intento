# Gestione Dichiarazioni d'Intento

Modulo Odoo per la gestione delle dichiarazioni d'intento dei fornitori.

## Descrizione

Questo modulo consente di gestire le dichiarazioni d'intento fornitori in Odoo. Una dichiarazione d'intento è un documento fiscale che permette di effettuare acquisti a tassazione 0%.

## Caratteristiche Principali

- **Modello Dichiarazione d'Intento**: Gestione completa delle dichiarazioni con codice, partner fornitore, validità temporale e plafond
- **Applicazione Automatica**: Quando si crea un ordine di acquisto, il sistema ricerca automaticamente una dichiarazione d'intento valida e la applica
- **Azzeramento Tasse**: Se un ordine ha una dichiarazione d'intento collegata, le tasse vengono automaticamente azzerate a 0%
- **Tracciamento Ordini**: Visualizzazione di tutti gli ordini associati a una dichiarazione d'intento e ammontare totale speso
- **Integrazione Ordini**: Aggiunta dei campi dichiarazione d'intento agli ordini di acquisto con snapshot del codice e data

## Modelli Dati

### dichiarazione.intento
Modello principale per la gestione delle dichiarazioni d'intento.

**Campi principali:**
- `code`: Codice univoco della dichiarazione (per fornitore)
- `partner_id`: Fornitore a cui è associata (criterio di filtro)
- `declaration_date`: Data di dichiarazione
- `date_start`: Data inizio validità (informativa)
- `date_end`: Data fine validità (informativa)
- `reference_year`: Anno di riferimento (informativo)
- `plafond`: Importo massimo autorizzato
- `fiscal_position_id`: Posizione fiscale da applicare (tasse 0%)
- `active`: Dichiarazione attiva/disattiva (criterio di filtro)
- `total_amount`: Ammontare totale ordini (calcolato automaticamente)
- `purchase_order_ids`: Ordini collegati (relazione inversa)

## Funzionamento

### Creazione Dichiarazione d'Intento

1. Accedere a "Acquisti > Dichiarazioni d'Intento"
2. Creare una nuova dichiarazione con i dati richiesti
3. Associare una posizione fiscale con tasse a 0%
4. Attivare la dichiarazione

### Applicazione Automatica agli Ordini

Quando si seleziona un fornitore in un ordine di acquisto:

1. Il sistema cerca una dichiarazione d'intento valida per quel fornitore
2. I criteri di ricerca sono:
   - Partner = fornitore dell'ordine
   - Attiva = True
3. Se trovata, la dichiarazione viene applicata automaticamente
4. Le tasse su tutte le righe vengono azzerate a 0%

### Visualizzazione Ammontare Ordini

Nella scheda della dichiarazione d'intento è possibile visualizzare:
- **total_amount**: Importo totale speso
- **Tab Ordini d'Acquisto**: Elenco completo di tutti gli ordini collegati con dettagli

## Configurazione

### Posizione Fiscale

Per far funzionare correttamente il modulo, è necessario configurare una posizione fiscale con tasse a 0%:

1. Accedere a "Contabilità > Configurazione > Posizioni Fiscali"
2. Creare una nuova posizione (es. "Non Imponibile")
3. Configurare le mappature tasse per azzerare l'IVA
4. Associare questa posizione alla dichiarazione d'intento

## Filtri di Visualizzazione

Per impostazione predefinita, la lista delle dichiarazioni d'intento mostra solo quelle **attive**.

Per visualizzare le dichiarazioni disattivate, usare il filtro "Non Attive" nella vista di ricerca.

## Note Importanti

- Le dichiarazioni d'intento sono filtrate **solo in base al fornitore e allo stato attivo**, indipendentemente dalle date di validità.
- Le date di validità (date_start, date_end) e l'anno di riferimento sono campi informativi utilizzati per tracciamento e scopi amministrativi, non per l'applicazione automatica agli ordini.
- La selezione della dichiarazione avviene automaticamente quando si seleziona il fornitore nell'ordine di acquisto.

## File Principali

- `models/dichiarazione_intento.py`: Modello Dichiarazione d'Intento
- `models/purchase_order.py`: Estensioni per Purchase Order
- `models/res_partner.py`: Estensioni per Partner (relation inversa)
- `views/dichiarazione_intento_views.xml`: Viste della dichiarazione
- `views/purchase_order_views.xml`: Viste per ordine di acquisto
- `security/ir.model.access.csv`: Permessi di accesso

## Requisiti

- Odoo 19.0+
- Modulo base
- Modulo purchase

## Autore

Tommaso Sollo
