DROP TABLE IF EXISTS uzivatele_opravy;
DROP TABLE IF EXISTS opravy_polozky;
DROP TABLE IF EXISTS objednavky;
DROP TABLE IF EXISTS opravy;
DROP TABLE IF EXISTS polozky;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS typy_oprav;
DROP TABLE IF EXISTS uzivatele;
DROP TABLE IF EXISTS vozidla;

CREATE TABLE objednavky (
    id_objednavky        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    popis                TEXT NOT NULL,
    preferovany_termin   TEXT,
    datum_vzniku         TEXT NOT NULL,
    stav                 TEXT NOT NULL,
    typ_opravy_id_opravy INTEGER NOT NULL,
    vozidlo_id_vozidla   INTEGER NOT NULL,
    poznamka             TEXT,
    FOREIGN KEY (typ_opravy_id_opravy) REFERENCES typy_oprav (id_opravy),
    FOREIGN KEY (vozidlo_id_vozidla) REFERENCES vozidla (id_vozidla)
);

CREATE TABLE opravy (
    id_opravy                INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    popis_provedenych_praci  TEXT NOT NULL,
    cas_straveny_na_oprave   REAL NOT NULL,
    datum_zacatku_opravy     TEXT NOT NULL,
    datum_konce_opravy       TEXT,
    objednavka_id_objednavky INTEGER NOT NULL,
    FOREIGN KEY (objednavka_id_objednavky) REFERENCES objednavky (id_objednavky)
);

CREATE TABLE opravy_polozky (
    id_opravy               INTEGER NOT NULL,
    id_polozky              INTEGER NOT NULL,
    pocet_pouzitych_kusu    INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (id_opravy, id_polozky),
    FOREIGN KEY (id_opravy) REFERENCES opravy (id_opravy),
    FOREIGN KEY (id_polozky) REFERENCES polozky (id_polozky)
);

CREATE TABLE polozky (
    id_polozky           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nazev                TEXT NOT NULL,
    vyrobce              TEXT NOT NULL,
    nakupni_cena         REAL NOT NULL,
    pocet_kusu           INTEGER NOT NULL,
    prodejni_cena        REAL NOT NULL,
    minimalni_pocet_kusu INTEGER NOT NULL,
    poznamka             TEXT
);

CREATE TABLE role (
    id_role INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nazev   TEXT NOT NULL,
    popis   TEXT
);

CREATE TABLE typy_oprav (
    id_opravy INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nazev     TEXT NOT NULL,
    popis     TEXT
);

CREATE TABLE uzivatele (
    id_uzivatele INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
    jmeno        TEXT NOT NULL,
    prijmeni     TEXT NOT NULL,
    email        TEXT NOT NULL,
    heslo        TEXT NOT NULL,
    role_id_role INTEGER NOT NULL,
    FOREIGN KEY (role_id_role) REFERENCES role (id_role)
);

CREATE TABLE uzivatele_opravy (
    id_opravy    INTEGER NOT NULL,
    id_uzivatele INTEGER NOT NULL,
    PRIMARY KEY (id_opravy, id_uzivatele),
    FOREIGN KEY (id_opravy) REFERENCES opravy (id_opravy),
    FOREIGN KEY (id_uzivatele) REFERENCES uzivatele (id_uzivatele)
);

CREATE TABLE vozidla (
    id_vozidla            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    spz                   TEXT NOT NULL,
    znacka_vozidla        TEXT NOT NULL,
    typ_vozidla           TEXT NOT NULL,
    uzivatel_id_uzivatele INTEGER NOT NULL,
    FOREIGN KEY (uzivatel_id_uzivatele) REFERENCES uzivatele (id_uzivatele)
);



INSERT INTO objednavky (id_objednavky, popis, preferovany_termin, datum_vzniku, stav, typ_opravy_id_opravy, vozidlo_id_vozidla) VALUES (1, 'Potřebuji vyměnit olej v automatické převodovce.', '2025-01-10', '2024-12-30', 'čekající', 3, 3);

INSERT INTO opravy (id_opravy, popis_provedenych_praci, cas_straveny_na_oprave, datum_zacatku_opravy, datum_konce_opravy, objednavka_id_objednavky) VALUES (1, 'Vyměněn olej v automatické převodovce Lamborghini.', 18, '2024-12-30', '2024-12-31', 1);

INSERT INTO opravy_polozky (id_opravy, id_polozky, pocet_pouzitych_kusu) VALUES (1, 4, 3);

INSERT INTO polozky (id_polozky, nazev, vyrobce, nakupni_cena, pocet_kusu, prodejni_cena, minimalni_pocet_kusu, poznamka) VALUES (1, 'Motorový olej W222 1L', 'VinDiesel s.r.o.', 1000, 10, 1600, 10, 'tohle je velmi kvalitní motorový olej');
INSERT INTO polozky (id_polozky, nazev, vyrobce, nakupni_cena, pocet_kusu, prodejni_cena, minimalni_pocet_kusu, poznamka) VALUES (2, 'Šroub 3mm', 'Ocelárny Hnivín a.s.', 20, 39, 30, 30, 'typ A872C');
INSERT INTO polozky (id_polozky, nazev, vyrobce, nakupni_cena, pocet_kusu, prodejni_cena, minimalni_pocet_kusu, poznamka) VALUES (3, 'Vzduchový filtr RACE', 'PROGEN Tech', 279, 15, 359, 10, 'pro vyšší výkon');
INSERT INTO polozky (id_polozky, nazev, vyrobce, nakupni_cena, pocet_kusu, prodejni_cena, minimalni_pocet_kusu, poznamka) VALUES (4, 'Olej do převodovky Lamborghini 2L', 'Lamborghini Bologna', 8290, 5, 9900, 2, null);

INSERT INTO role (id_role, nazev, popis) VALUES (1, 'Manažer', null);
INSERT INTO role (id_role, nazev, popis) VALUES (2, 'Technik', null);
INSERT INTO role (id_role, nazev, popis) VALUES (3, 'Administrativní pracovník', null);
INSERT INTO role (id_role, nazev, popis) VALUES (4, 'Zákazník', null);

INSERT INTO typy_oprav (id_opravy, nazev, popis) VALUES (1, 'Výměna oleje', 'Běžná výměna oleje + olejového filtru.');
INSERT INTO typy_oprav (id_opravy, nazev, popis) VALUES (2, 'Výměna filtrů', 'Vzduchový filtr, kabinový filtr, pylový filtr.');
INSERT INTO typy_oprav (id_opravy, nazev, popis) VALUES (3, 'Výměna oleje v převodovce', 'Výměna oleje v automatické převodovce.');

INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (1, 'Pepa', 'Manazeros', 'manazer@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 1);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (2, 'Marek', 'Nesvatbos', 'technik1@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 2);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (3, 'Feros', 'Technikosak', 'technik2@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 3);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (4, 'Adriana', 'Ministrakova', 'adprac1@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 3);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (5, 'Ferda', 'Klient', 'zakaznik1@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 4);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (7, 'Lukas', 'Alan', 'alan@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 4);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (8, 'Lilie', 'Fialova', 'fialova@hr.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 3);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (9, 'Franta', 'Zákazníček', 'zakaznicek@seznam.cz', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 4);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (10, 'Malman', 'Irkos', 'irko@gmail.com', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 4);
INSERT INTO uzivatele (id_uzivatele, jmeno, prijmeni, email, heslo, role_id_role) VALUES (11, 'Ferkus', 'Lakatos', 'lakatos@gmail.com', '401c68676bcb8f7532423c3f5c22d9877792bbf3380087749c9a8f50234d20ee', 3);

INSERT INTO uzivatele_opravy (id_opravy, id_uzivatele) VALUES (1, 2);

INSERT INTO vozidla (id_vozidla, spz, znacka_vozidla, typ_vozidla, uzivatel_id_uzivatele) VALUES (1, '8B13953', 'Škoda', 'Osobní automobil', 7);
INSERT INTO vozidla (id_vozidla, spz, znacka_vozidla, typ_vozidla, uzivatel_id_uzivatele) VALUES (2, 'IAMH4PPY', 'Mercedes-Benz', 'Osobní automobil', 7);
INSERT INTO vozidla (id_vozidla, spz, znacka_vozidla, typ_vozidla, uzivatel_id_uzivatele) VALUES (3, 'T00LATE1', 'Lamborghini', 'Osobní automobil', 7);
INSERT INTO vozidla (id_vozidla, spz, znacka_vozidla, typ_vozidla, uzivatel_id_uzivatele) VALUES (4, 'TIR11111', 'MAN', 'Tahač', 7);



