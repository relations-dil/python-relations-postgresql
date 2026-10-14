import unittest
import unittest.mock

import relations
from relations_postgresql import *


class TestCOLUMN(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        field = relations.Field(bool, name="flag", default=True)
        ddl = COLUMN(field.define())
        self.assertEqual(ddl.migration["default"], 1)

    def test_kind(self):

        field = relations.Field(int, store="id", default=1, none=False)
        definition = {
            "store": "_id",
            "kind": "float",
            "default": 1.25,
            "none": True
        }
        ddl = COLUMN(field.define(), definition)

        sql = []
        ddl.kind(sql)
        self.assertEqual(sql, ["""ALTER "id" TYPE INT8 USING "id"::INT8"""])

    def test_modify(self):

        # an id that stops being an auto int loses the sequence default BIGSERIAL gave it

        definition = relations.Field(int, name="id", auto=True).define()

        ddl = COLUMN(migration={"kind": "str", "none": False}, definition=definition)
        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER "id" TYPE VARCHAR(255) USING "id"::VARCHAR(255),ALTER "id" SET NOT NULL,ALTER "id" DROP DEFAULT""")

        ddl = COLUMN(migration={"auto": False}, definition=definition)
        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER "id" DROP DEFAULT""")

        ddl = COLUMN(migration={"kind": "str", "default": None}, definition=definition)
        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER "id" TYPE VARCHAR(255) USING "id"::VARCHAR(255),ALTER "id" DROP DEFAULT""")

        ddl = COLUMN(migration={"kind": "str", "none": False}, definition=definition)
        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER "id" TYPE VARCHAR(255) USING "id"::VARCHAR(255),
ALTER "id" SET NOT NULL,
ALTER "id" DROP DEFAULT""")

        # still an auto int, or not auto to begin with, nothing to drop

        ddl = COLUMN(migration={"none": False}, definition=definition)
        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER "id" SET NOT NULL""")

        ddl = COLUMN(migration={"kind": "str"}, definition=relations.Field(int, name="id").define())
        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER "id" TYPE VARCHAR(255) USING "id"::VARCHAR(255)""")

    def test_generate(self):

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"flag" BOOLEAN""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"id" INT8""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id", auto=True)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"id" BIGSERIAL""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"_price" FLOAT8 NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"_name" VARCHAR(255) NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """"_data" JSONB NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str")

        ddl.generate()
        self.assertEqual(ddl.sql, """"data__a__0___1____2_____3" VARCHAR(255) GENERATED ALWAYS AS (("data"#>>'{a,0,-1,"2","-3"}')::VARCHAR(255)) STORED""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "flag" BOOLEAN""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "id" INT8""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "_price" FLOAT8 NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "_name" VARCHAR(255) NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "_data" JSONB NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str", added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD "data__a__0___1____2_____3" VARCHAR(255) GENERATED ALWAYS AS (("data"#>>'{a,0,-1,"2","-3"}')::VARCHAR(255)) STORED""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, store="id", default=1, none=False)
        definition = {
            "store": "_id",
            "kind": "float",
            "default": 1.25,
            "none": True
        }
        ddl = COLUMN(field.define(), definition)

        ddl.generate()
        self.assertEqual(ddl.sql, """RENAME "_id" TO "id",ALTER "id" TYPE INT8 USING "id"::INT8,ALTER "id" SET DEFAULT 1,ALTER "id" SET NOT NULL""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="data", default={"a": 1}, none=False)
        definition = {
            "store": "data",
            "kind": "dict"
        }
        ddl = COLUMN(field.define(), definition)

        ddl.generate()
        self.assertEqual(ddl.sql, """RENAME "data" TO "data",ALTER "data" TYPE JSONB USING "data"::JSONB,ALTER "data" SET DEFAULT '{"a": 1}',ALTER "data" SET NOT NULL""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(definition=field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP "flag\"""")
        self.assertEqual(ddl.args, [])
