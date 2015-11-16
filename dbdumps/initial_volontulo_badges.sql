CREATE TABLE "volontulo_badge" IF NOT EXISTS (
  id serial,
  name varchar,
  slug varchar,
  priority int4
);
DELETE FROM "volontulo_badge" WHERE slug = 'volunteer' OR slug = 'participant' OR slug = 'prominent-participant';

INSERT INTO "volontulo_badge"(id, name, slug, priority) VALUES (3, 'Wolontariusz', 'volunteer', 1);
INSERT INTO "volontulo_badge"(id, name, slug, priority) VALUES (2, 'Wybitny Uczestnik', 'prominent-participant', 3);
INSERT INTO "volontulo_badge"(id, name, slug, priority) VALUES (1, 'Uczestnik', 'participant', 2);

