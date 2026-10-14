import unittest
import unittest.mock

import os
import psycopg2.extras

import relations
from relations_postgresql import *


class TestExecute(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        connection = psycopg2.connect(
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS "unittest"')
        cursor.execute('CREATE DATABASE "unittest"')

        self.connection = psycopg2.connect(
            dbname="unittest",
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute('CREATE SCHEMA "unit"')
        cursor.execute('CREATE SCHEMA "test"')

    def tearDown(self):

        self.connection.close()

        connection = psycopg2.connect(
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        connection.autocommit = True

        connection.cursor().execute('DROP DATABASE IF EXISTS "unittest"')

    def  check(self, value, **kwargs):

        cursor = self.connection.cursor()

        query = SELECT(
            "name"
        ).FROM(
            "unit.meta"
        ).WHERE(
            **kwargs
        )

        query.generate()

        cursor.execute(query.sql, query.args)

        if cursor.rowcount != 1:
            name = None
        else:
            name = cursor.fetchone()["name"]

        self.assertEqual(name, value, query.sql)

    def execute(self, sql):

        cursor = self.connection.cursor()

        for statement in sql.split(";\n"):
            if statement:
                try:
                    cursor.execute(statement)
                except:
                    self.fail(statement)

    def test_execute(self):

        class Meta(relations.Model):

            SCHEMA = "unit"

            id = int,{"auto": True}
            name = str
            flag = bool
            spend = float
            people = set
            stuff = list
            things = dict, {"extract": "for__0____1"}
            push = str

        cursor = self.connection.cursor()

        # create

        ddl = TABLE(Meta.thy().define())

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # query

        query = INSERT(
            "unit.meta"
        ).VALUES(**{
            "name": "yep",
            "flag": True,
            "spend": 1.1,
            "people": {"tom"},
            "stuff": [1, None],
            "things": {"a": 1}
        }).VALUES(
            name="dive",
            flag=False,
            spend=3.5,
            people={"tom", "mary"},
            stuff=[1, 2, 3, None],
            things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]}
        )

        query.generate()

        cursor.execute(query.sql, query.args)

        self.check("yep", flag=True)

        self.check("dive", flag=False)

        self.check("dive", people={"tom", "mary"})

        self.check("dive", things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]})

        self.check("dive", stuff__1=2)

        self.check("dive", things__a__b__0=1)

        self.check("dive", things__a__c__like="su")

        self.check("yep", things__a__b__null=True)

        self.check("dive", things____4=5)

        self.check(None, things__a__b__0__gt=1)

        self.check(None, things__a__c__not_like="su")

        self.check(None, things__a__d__null=False)

        self.check(None, things____4=6)

        self.check("dive", things__a__b__has=1)

        self.check(None, things__a__b__has=[1, 3])

        self.check("dive", things__a__b__not_has=[1, 3], things__a__b__null=False)

        self.check(None, name="yep", things__a__b__not_has=[1, 3])

        self.check("dive", things__a__b__any=[1, 3])

        self.check(None, things__a__b__any=[4, 3])

        self.check("dive", things__a__b__all=[2, 1])

        self.check(None, things__a__b__all=[3, 2, 1])

        self.check("dive", people__has="mary")

        self.check(None, people__has="dick")

        self.check("dive", people__any=["mary", "dick"])

        self.check(None, people__any=["harry", "dick"])

        self.check("dive", people__all=["mary", "tom"])

        self.check(None, people__all=["tom", "dick", "mary"])

        # modify

        ## schema

        definition = Meta.thy().define()

        Meta.SCHEMA = "test"

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        ## store

        definition = Meta.thy().define()

        Meta.NAME = "metar"

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # add field

        definition = Meta.thy().define()

        Meta.added = int

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # change kind

        definition = Meta.thy().define()

        Meta.added = float

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # change kind

        definition = Meta.thy().define()

        delattr(Meta, 'added')
        Meta.adding = float

        migration = {
            "fields": {
                "change": {
                    "added": {
                        "name": "adding"
                    }
                }
            }
        }

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # remove field

        definition = Meta.thy().define()

        delattr(Meta, 'adding')

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # add index

        definition = Meta.thy().define()

        Meta.INDEX = 'spend'

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # rename index

        definition = Meta.thy().define()

        Meta.INDEX = {
            "spending": ['spend']
        }

        migration = {
            "index": {
                "rename": {
                    "spend": "spending"
                }
            }
        }

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # drop index

        definition = Meta.thy().define()

        Meta.INDEX = None

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # add unique

        definition = Meta.thy().define()

        Meta.UNIQUE = {
            'name': ['name'],
            'spend': ['spend']
        }

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # rename unique

        definition = Meta.thy().define()

        Meta.UNIQUE =  {
            'name': ['name'],
            'spending': ['spend']
        }

        migration = {
            "unique": {
                "rename": {
                    "spend": "spending"
                }
            }
        }

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        # drop unique

        definition = Meta.thy().define()

        Meta.UNIQUE = {
            'name': ['name']
        }

        migration = Meta.thy().migrate(definition)

        ddl = TABLE(migration, definition)

        ddl.generate(indent=2)

        self.execute(ddl.sql)

        class Slug(relations.Model):

            SCHEMA = "unit"

            id = str
            name = str

        ddl = TABLE(Slug.thy().define())
        ddl.generate(indent=2)
        self.execute(ddl.sql)

        cursor = self.connection.cursor()

        # ids that differ only by case are different ids, a repeat is refused

        cursor.execute("""INSERT INTO "unit"."slug" ("id","name") VALUES ('abc.pet.main.unum','lower'),('ABC.PET.MAIN.UNUM','upper')""")
        cursor.execute("""SELECT "id" FROM "unit"."slug" ORDER BY "id" """)
        self.assertEqual([row["id"] for row in cursor.fetchall()], ["ABC.PET.MAIN.UNUM", "abc.pet.main.unum"])

        self.assertRaises(psycopg2.IntegrityError, cursor.execute, """INSERT INTO "unit"."slug" ("id","name") VALUES ('abc.pet.main.unum','again')""")

        class Num(relations.Model):

            SCHEMA = "unit"

            id = int, {"auto": True}
            name = str

        ddl = TABLE(Num.thy().define())
        ddl.generate(indent=2)
        self.execute(ddl.sql)

        cursor = self.connection.cursor()

        cursor.execute("""INSERT INTO "unit"."num" ("name") VALUES ('one')""")

        # int to string, the sequence is no longer the default

        ddl = TABLE(
            migration={"fields": {"change": {"id": {"kind": "str", "auto": False, "none": False, "readonly": True}}}},
            definition=Num.thy().define()
        )
        ddl.generate(indent=2)
        self.execute(ddl.sql)

        cursor.execute("""INSERT INTO "unit"."num" ("id","name") VALUES ('abc','lower'),('ABC','upper')""")
        cursor.execute("""SELECT "id" FROM "unit"."num" ORDER BY "id" """)
        self.assertEqual([row["id"] for row in cursor.fetchall()], ["1", "ABC", "abc"])

        # an insert without an id is refused, it doesn't get the next number

        self.assertRaises(psycopg2.IntegrityError, cursor.execute, """INSERT INTO "unit"."num" ("name") VALUES ('none')""")
