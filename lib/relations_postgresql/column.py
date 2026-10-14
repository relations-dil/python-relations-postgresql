"""
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_postgresql

class COLUMN(relations_postgresql.DDL, relations_sql.COLUMN):
    """
    COLUMN DDL
    """

    KINDS = {
        "bool": "BOOLEAN",
        "int": "INT8",
        "float": "FLOAT8",
        "str": "VARCHAR(255)",
        "json": "JSONB"
    }

    COLUMN_NAME = relations_postgresql.COLUMN_NAME

    STORE = """RENAME %s TO %s"""
    AUTO = """BIGSERIAL"""
    EXTRACT = """GENERATED ALWAYS AS ((%s)::%s) STORED"""
    SET_DEFAULT = """ALTER %s SET DEFAULT %s"""
    UNSET_DEFAULT = """ALTER %s DROP DEFAULT"""
    SET_NONE = """ALTER %s SET NOT NULL"""
    UNSET_NONE = """ALTER %s DROP NOT NULL"""

    def extract(self, kind, sql, **kwargs):
        """
        Get extract DDL
        """

        sql.append(self.KINDS.get(self.migration['kind'], self.KINDS["json"]))

        name, path = self.COLUMN_NAME.split(self.migration["store"])
        sql.append(self.EXTRACT % (self.PATH % (self.quote(name), self.str(self.walk(path))), self.KINDS.get(kind, self.KINDS["json"])))

    def kind(self, sql):
        """
        Modifies the kind
        """

        cast = self.KINDS.get(self.migration.get("kind", self.definition["kind"]), self.KINDS["json"])

        sql.append(f'ALTER {self.name()} TYPE {cast} USING {self.name()}::{cast}')

    def modify(self, indent=0, count=0, pad=' ', **kwargs):
        """
        MODIFY DLL, an id that stops being an auto int also loses the sequence default BIGSERIAL gave it
        """

        super().modify(indent=indent, count=count, pad=pad, **kwargs)

        migration = self.migration

        stops = migration.get("auto") is False or migration.get("kind", "int") != "int"

        if self.definition.get("auto") and "default" not in migration and stops:

            current = pad * (count * indent)
            delimitter = f",\n{current}" if indent else ','

            self.sql = delimitter.join(filter(None, [self.sql, self.UNSET_DEFAULT % self.name()]))
