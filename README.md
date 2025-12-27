# Gestione Dichiarazioni d'Intento

Modulo Odoo per la gestione delle dichiarazioni d'intento dei fornitori.

## 📋 Descrizione

Questo modulo consente di gestire le dichiarazioni d'intento fornitori in Odoo. Una **dichiarazione d'intento** è un documento fiscale che permette di effettuare acquisti a tassazione **0%**.

## ✨ Caratteristiche Principali

- **Modello Dichiarazione d'Intento**: Gestione completa delle dichiarazioni con codice, partner fornitore, validità temporale e plafond
- **Applicazione Automatica**: Quando si crea un ordine di acquisto, il sistema ricerca automaticamente una dichiarazione d'intento valida e la applica
- **Azzeramento Tasse**: Se un ordine ha una dichiarazione d'intento collegata, le tasse vengono automaticamente azzerate a 0%
- **Tracciamento Ordini**: Visualizzazione di tutti gli ordini associati a una dichiarazione d'intento e ammontare totale speso
- **Integrazione Ordini**: Aggiunta dei campi dichiarazione d'intento agli ordini di acquisto con snapshot del codice e data
- **Visualizzazione Report**: Nei report PDF di purchase order viene visualizzata la dichiarazione d'intento collegata (codice e data)

## 📊 Modelli Dati

### dichiarazione.intento

Modello principale per la gestione delle dichiarazioni d'intento.

#### Campi principali:

| Campo | Descrizione | Tipo |
|-------|-------------|------|
| `code` | Codice univoco della dichiarazione (per fornitore) | Char |
| `partner_id` | Fornitore a cui è associata (criterio di filtro) | Many2one |
| `declaration_date` | Data di dichiarazione | Date |
| `date_start` | Data inizio validità (informativa) | Date |
| `date_end` | Data fine validità (informativa) | Date |
| `reference_year` | Anno di riferimento (informativo) | Integer |
| `plafond` | Importo massimo autorizzato | Float |
| `fiscal_position_id` | Posizione fiscale da applicare (tasse 0%) | Many2one |
| `active` | Dichiarazione attiva/disattivata (criterio di filtro) | Boolean |
| `total_amount` | Ammontare totale ordini (calcolato automaticamente) | Float |
| `purchase_order_ids` | Ordini collegati (relazione inversa) | One2many |

## ⚙️ Funzionamento

### Creazione Dichiarazione d'Intento

1. Accedere a **Acquisti > Dichiarazioni d'Intento**
2. Creare una nuova dichiarazione con i dati richiesti
3. Associare una posizione fiscale con tasse a 0%
4. Attivare la dichiarazione

### Applicazione Automatica agli Ordini

Quando si seleziona un fornitore in un ordine di acquisto:

1. Il sistema cerca una dichiarazione d'intento valida per quel fornitore
2. I criteri di ricerca sono:
   - **Partner** = fornitore dell'ordine
   - **Attiva** = Sì
   - **Anno di Riferimento** = anno corrente
3. Se trovata, la dichiarazione viene applicata automaticamente (viene selezionata l'ultima per data inizio validità)
4. Le tasse su tutte le righe vengono azzerate a 0%

### Visualizzazione Ammontare Ordini

Nella scheda della dichiarazione d'intento è possibile visualizzare:
- **Ammontare IVA Ordini (simulata)**: Importo simulato dell'IVA al 22% su tutti gli ordini collegati (calcolato come 0.22 × somma dei totali ordini)
- **Scheda Ordini d'Acquisto**: Elenco completo di tutti gli ordini collegati con dettagli

## 🔧 Configurazione

### Posizione Fiscale

Per far funzionare correttamente il modulo, è necessario configurare una posizione fiscale con tasse a 0%:

1. Accedere a **Contabilità > Configurazione > Posizioni Fiscali**
2. Creare una nuova posizione (es. "Non Imponibile" o "Dichiarazione d'Intento")
3. Configurare le mappature tasse per azzerare l'IVA
4. Associare questa posizione alla dichiarazione d'intento

### Filtri di Visualizzazione

Per impostazione predefinita, la lista delle dichiarazioni d'intento mostra solo quelle **attive**.

Per visualizzare le dichiarazioni disattivate, usare il filtro **"Non Attive"** nella vista di ricerca.

## ⚠️ Note Importanti

- Le dichiarazioni d'intento sono filtrate per **fornitore**, **stato attivo**, e **anno di riferimento (anno corrente)**
- L'anno di riferimento è un criterio di filtro per l'applicazione automatica agli ordini
- Le date di validità (`date_start`, `date_end`) sono campi informativi utilizzati per tracciamento e scopi amministrativi, **non** per l'applicazione automatica
- La selezione della dichiarazione avviene **automaticamente** quando si seleziona il fornitore nell'ordine di acquisto, scegliendo l'ultima per data inizio validità
- Una volta applicata la dichiarazione, le tasse su tutte le righe dell'ordine vengono azzerate a 0%
- Il campo **Ammontare IVA Ordini (simulata)** calcola l'IVA al 22% sui totali degli ordini collegati, non il semplice importo totale

## 📁 File Principali

| File | Descrizione |
|------|-------------|
| `models/dichiarazione_intento.py` | Modello Dichiarazione d'Intento |
| `models/purchase_order.py` | Estensioni per Purchase Order |
| `models/res_partner.py` | Estensioni per Partner (relazione inversa) |
| `views/dichiarazione_intento_views.xml` | Viste della dichiarazione (form, list, search) |
| `views/purchase_order_views.xml` | Viste per ordine di acquisto |
| `views/res_partner_views.xml` | Scheda dichiarazioni nel partner |
| `views/menus.xml` | Menu di navigazione |
| `security/ir.model.access.csv` | Permessi di accesso ai modelli |

## 📦 Requisiti

- **Odoo**: 19.0+
- **Moduli dipendenti**: `base`, `purchase`
- **Docker**: Per l'installazione containerizzata (opzionale)
- **PostgreSQL**: 15+ (se si usa Docker Compose)

## 🚀 Installazione e Avvio

### Con Docker Compose (Consigliato)

Il modulo è configurato per l'installazione automatica tramite Docker Compose:

```bash
docker-compose up -d
```

Questo comando:
1. Crea un container PostgreSQL per il database
2. Crea un container Odoo 19.0
3. Installa automaticamente i moduli `base` e `dichiarazioni_intento`

Odoo sarà accessibile all'indirizzo: **http://localhost:8069**

### Manuale

1. Posizionare la cartella `dichiarazioni_intento` in `/addons/`
2. Accedere a Odoo e andare su **App**
3. Cliccare su **Aggiorna lista moduli**
4. Cercare "Dichiarazioni d'Intento" o "dichiarazioni"
5. Cliccare su **Installa**

## 🔍 Note Tecniche

- L'ordine delle viste XML è importante: la vista di ricerca deve essere definita prima dell'azione che la referenzia
- I permessi di accesso sono configurati nel file `security/ir.model.access.csv`
- Tutti i commenti nel codice sono in italiano per coerenza con il modulo
- Le relazioni Many2one filtrano automaticamente i fornitori attivi
- I calcoli automatici del `total_amount` avvengono tramite il metodo `@api.depends`

## 📝 Autore

**Tommaso Sollo**
