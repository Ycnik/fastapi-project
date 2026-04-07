DROP INDEX IF EXISTS
    ausruestung_soldat_id_idx,
    ausruestung_serienummer_idx,
    verletzung_soldat_id_idx,
    soldat_nachname_idx;

DROP TABLE IF EXISTS
    ausruestung,
    verletzung,
    soldat CASCADE;

DROP TYPE IF EXISTS
    geschlecht,
    rang,
    schweregrad,
    waffe;    
