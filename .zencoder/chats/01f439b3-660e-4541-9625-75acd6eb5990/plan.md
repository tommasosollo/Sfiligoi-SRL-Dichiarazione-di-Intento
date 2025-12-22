# Plan for Odoo Module: sfiligoi_intento

- [x] **Phase 1: Module Structure & Manifest**
    - [x] Create module directory `sfiligoi_intento`
    - [x] Create `__init__.py` and `__manifest__.py`
- [x] **Phase 2: Models Implementation**
    - [x] Create `models/dichiarazione_intento.py` (Main model)
    - [x] Create `models/res_partner.py` (Extension)
    - [x] Create `models/purchase_order.py` (Extension)
    - [x] Create `models/__init__.py`
- [x] **Phase 3: Security**
    - [x] Create `security/ir.model.access.csv`
- [x] **Phase 4: Views & Menus**
    - [x] Create `views/dichiarazione_intento_views.xml` (Tree, Form, Search)
    - [x] Create `views/res_partner_views.xml` (Partner extension)
    - [x] Create `views/purchase_order_views.xml` (Purchase extension)
    - [x] Create `views/menus.xml`
- [x] **Phase 5: Business Logic Verification**
    - [x] Verify `_onchange` logic in `purchase.order`
    - [x] Verify constraints and validations
