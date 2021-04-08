from peewee import *


db = SqliteDatabase("comp_db.db")


class BaseModel(Model):
    id = PrimaryKeyField()
    class Meta:
        database = db
        order_by = "id"

class Titul(BaseModel):
    # id_comp = PrimaryKeyField()
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
    # id_r_list = PrimaryKeyField()
    number = IntegerField()
    r_list = IntegerField()
    r_fname = CharField(50)
    r_bithday = DateField()
    r_city = CharField(0)

    class Meta:
        db_table = "r_lists"
        order_by = "r_fname"


class City(BaseModel):
    pass
    # id_city = PrimaryKeyField()
    # city = CharField(0)
    #
    #
    # class Meta:
    #     db_table = "cities"
    #     order_by = "city"


class Region(BaseModel):
     pass
    # id_region = PrimaryKeyField()
    # region = CharField()
    # city = ForeignKeyField(City, to_field="id_city")
    # class Meta:
    #     db_table = "regions"
    #     order_by = "region"
