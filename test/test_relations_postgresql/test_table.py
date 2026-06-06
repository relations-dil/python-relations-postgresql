import unittest
import unittest.mock

import relations
from relations_postgresql import *


class Simple(relations.Model):
    id = int
    name = str

class Meta(relations.Model):
    id = int, {"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}
    push = str, {"inject": "stuff___1__relations.io____1"}
    tied = str, {"store": False}

    INDEX = "spend"


class TestTABLE(unittest.TestCase):

    maxDiff = None

    def test_name(self):

        ddl = TABLE(schema="people", name="stuff", definition={"schema": "persons", "name": "things"})

        self.assertEqual(ddl.name(), """"people"."stuff\"""")
        self.assertEqual(ddl.name(state="definition"), """"persons"."things\"""")
        self.assertEqual(ddl.name(state={"name": "definition", "schema": "migration"}), """"people"."things\"""")
        self.assertEqual(ddl.name(state={"name": "definition", "schema": "migration"}, rename=True), """"things\"""")

    def test_create(self):

        ddl = TABLE(**Meta.thy().define())
        ddl.args = []

        ddl.create(indent=2)
        self.assertEqual(ddl.sql, """CREATE TABLE IF NOT EXISTS "meta" (
  "id" BIGSERIAL,
  "name" VARCHAR(255) NOT NULL,
  "flag" BOOLEAN,
  "spend" FLOAT8,
  "people" JSONB NOT NULL,
  "stuff" JSONB NOT NULL,
  "things" JSONB NOT NULL,
  "things__for__0____1" VARCHAR(255) GENERATED ALWAYS AS (("things"#>>'{for,0,"1"}')::VARCHAR(255)) STORED,
  PRIMARY KEY ("id")
);

CREATE INDEX "meta_spend" ON "meta" ("spend");

CREATE UNIQUE INDEX "meta_name" ON "meta" ("name");
""")

    def test_schema(self):

        sql = []

        ddl = TABLE(
            migration={
                "name": "good",
                "schema": "dreaming"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.schema(sql)
        self.assertEqual(sql, ["""ALTER TABLE "scheming"."evil" SET SCHEMA "dreaming\""""])

    def test_store(self):

        sql = []

        ddl = TABLE(
            migration={
                "name": "good"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.store(sql)
        self.assertEqual(sql, ["""ALTER TABLE "scheming"."evil" RENAME TO "good\""""])

    def test_modify(self):

        ddl = TABLE(
            migration={
                "name": "good",
                "schema": "dreaming"
            },
            definition={
                "name": "evil",
                "schema": "scheming"
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER TABLE "scheming"."evil" SET SCHEMA "dreaming";

ALTER TABLE "dreaming"."evil" RENAME TO "good";
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "add": Meta.thy().define()["fields"][-3:]
                }
            },
            definition=Simple.thy().define()
        )

        ddl.generate()
        self.assertEqual(ddl.sql,
            """ALTER TABLE "simple" ADD "things" JSONB NOT NULL,"""
            """ADD "things__for__0____1" VARCHAR(255) GENERATED ALWAYS AS (("things"#>>'{for,0,"1"}')::VARCHAR(255)) STORED;\n"""
        )
        self.assertEqual(ddl.args, [])

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE "simple"
  ADD "things" JSONB NOT NULL,
  ADD "things__for__0____1" VARCHAR(255) GENERATED ALWAYS AS (("things"#>>'{for,0,"1"}')::VARCHAR(255)) STORED;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql,
            """ALTER TABLE "yep" """
            """ALTER "spend" SET DEFAULT 1.25,"""
            """RENAME "things" TO "thingies","""
            """RENAME "things__for__0____1" TO "thingies__for__0____1","""
            """ALTER "thingies__for__0____1" TYPE VARCHAR(255) USING "thingies__for__0____1"::VARCHAR(255);
"""
        )
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE "yep"
  ALTER "spend" SET DEFAULT 1.25,
  RENAME "things" TO "thingies",
  RENAME "things__for__0____1" TO "thingies__for__0____1",
  ALTER "thingies__for__0____1" TYPE VARCHAR(255) USING "thingies__for__0____1"::VARCHAR(255);
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER TABLE "yep" DROP "things",DROP "things__for__0____1";\n""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE "yep"
  DROP "things",
  DROP "things__for__0____1";
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "index": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "price"
                    ]
                },
                "unique": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "name"
                    ]
                }
            },
            definition={
                "name": "yep",
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """CREATE INDEX "yep_flag" ON "yep" ("flag");

DROP INDEX "yep_price";

CREATE UNIQUE INDEX "yep_flag" ON "yep" ("flag");

DROP INDEX "yep_name";
""")
        self.assertEqual(ddl.args, [])

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """CREATE INDEX "yep_flag" ON "yep" ("flag");

DROP INDEX "yep_price";

CREATE UNIQUE INDEX "yep_flag" ON "yep" ("flag");

DROP INDEX "yep_name";
""")
        self.assertEqual(ddl.args, [])

    def test_drop(self):

        ddl = TABLE(
            definition={
                "name": "yep"
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP TABLE IF EXISTS "yep";\n""")
        self.assertEqual(ddl.args, [])
