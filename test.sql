INSERT INTO categories (name) VALUES ('Teknologia');
INSERT INTO categories (name) VALUES ('Urheilu');
INSERT INTO categories (name) VALUES ('Matkailu');
INSERT INTO categories (name, is_secret) VALUES ('Salainen', TRUE);

INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 1, 'Uudet älypuhelimet', 'Mikä on paras älypuhelin vuonna 2024?');
INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 1, 'Tekoälyn tulevaisuus', 'Mitä mieltä olette tekoälyn vaikutuksista työllisyyteen?' );
INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 2, 'Jalkapallon MM-kisat', 'Kuka voittaa MM-kisat tänä vuonna?');
INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 2, 'Olympialaiset 2024', 'Mikä on suosikkilajisi olympialaisissa?');
INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 3, 'Parhaat matkakohteet Euroopassa', 'Mikä on paras matkakohde Euroopassa?');
INSERT INTO threads (user_id, category_id, name, content) VALUES (1, 3, 'Reppureissu Aasiassa', 'Mikä on paras reitti reppureissulle Aasiassa?');

INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (1, 1, 1, 'Olen kuullut hyvää uudesta mallista.');
INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (2, 1, 1, 'Tekoäly kehittyy todella nopeasti.');
INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (3, 1, 2, 'Odotan innolla finaalia!');
INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (4, 1, 2, 'Toivon, että Suomi voittaa kultaa.');
INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (5, 1, 3, 'Rakastan matkustamista Italiaan.');
INSERT INTO messages (thread_id, user_id, category_id, content) VALUES (6, 1, 3, 'Thaimaa on loistava kohde reppureissulle.');
