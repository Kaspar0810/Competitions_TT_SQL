from peewee import *


db = SqliteDatabase("comp_db.db")


class BaseModel(Model):
    id = PrimaryKeyField(unique=0)

    class Meta:
        database = db
        order_by = "id"

class Titul(BaseModel):
    name = CharField()
    vozrast = CharField()
    data_start = DateField()
    data_end = DateField()
    mesto = CharField(20)
    referee = CharField()
    kat_ref = CharField(10)
    secretary = CharField()
    kat_sek = CharField(10)

    class Meta:
        db_table = "tituls"

# class Listing(Model):
#     pass
#
#     class Meta:
#         pass

class R_list(BaseModel):
    number = IntegerField()
    r_list = IntegerField()
    r_fname = CharField(50)
    r_bithday = DateField()
    r_city = CharField(0)

    class Meta:
        db_table = "r_lists"


