SET default_tablespace = soldatspace;

DROP TYPE IF EXISTS geschlecht CASCADE;
DROP TYPE IF EXISTS rang CASCADE;
DROP TYPE IF EXISTS schweregrad CASCADE;
DROP TYPE IF EXISTS waffe CASCADE;

CREATE TYPE geschlecht AS ENUM ('MAENNLICH', 'WEIBLICH');

CREATE TYPE rang AS ENUM (
    'REKRUT',
    'SOLDAT',
    'ELITE-SOLDAT',
    'CAPTAIN',
    'KOMMANDANT'
);

CREATE TYPE schweregrad AS ENUM (
    'LEICHT',
    'MITTEL',
    'SCHWER',
    'KRITISCH'
);

CREATE TYPE waffe AS ENUM (
    'ODM_GEAR',
    'Schrotflinte',
    'Klinge'
);

CREATE TABLE IF NOT EXISTS soldat (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version       INTEGER NOT NULL DEFAULT 0,
    vorname       TEXT NOT NULL,
    nachname      TEXT NOT NULL,
    geburtsdatum  DATE CHECK (geburtsdatum < current_date),
    geschlecht    geschlecht,
    rang          rang,
    username      TEXT NOT NULL,
    erzeugt       TIMESTAMP NOT NULL,
    aktualisiert  TIMESTAMP NOT NULL
);

-- default: btree
CREATE INDEX IF NOT EXISTS soldat_nachname_idx ON soldat(nachname);

CREATE TABLE IF NOT EXISTS ausruestung (
    id          INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    waffe         waffe NOT NULL,
    seriennummer   TEXT NOT NULL,
    soldat_id  INTEGER NOT NULL REFERENCES soldat ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ausruestung_soldat_id_idx ON ausruestung(soldat_id);
CREATE INDEX IF NOT EXISTS ausruestung_seriennummer_idx ON ausruestung(seriennummer);

CREATE TABLE IF NOT EXISTS verletzung (
    id          INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    verletzungsbezeichnung    TEXT NOT NULL,
    behandelt   boolean NOT NULL,
    schweregrad   schweregrad NOT NULL,
    verletzungsdatum  DATE NOT NULL CHECK (verletzungsdatum <= current_date),
    soldat_id  INTEGER NOT NULL REFERENCES soldat ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS verletzung_soldat_id_idx ON verletzung(soldat_id);
