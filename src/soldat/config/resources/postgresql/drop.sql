DROP INDEX IF EXISTS
    ausruestung_soldat_id_idx,
    ausruestung_serienummer_idx,
    verletzungen_soldat_id_idx,
    soldat_nachname_idx;

DROP TABLE IF EXISTS
    verletzung,
    ausruestung,
    soldat;

DROP TYPE IF EXISTS
    geschlecht,
    rang,
    schweregrad,
    waffe;    
