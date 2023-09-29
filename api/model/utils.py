from api import db


def create_join_table(join_table_name: str, table_name_1: str, table_name_2: str):
    return db.Table(
        join_table_name,
        db.Column(
            f"{table_name_1}_id",
            db.Integer,
            db.ForeignKey(f"{table_name_1}.id"),
            primary_key=True,
        ),
        db.Column(
            f"{table_name_2}_id",
            db.Integer,
            db.ForeignKey(f"{table_name_2}.id"),
            primary_key=True,
        ),
    )
