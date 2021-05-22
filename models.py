from peewee import *


db = SqliteDatabase("comp_db.db")


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class Title(BaseModel):
    name = CharField()
    sredi = CharField()
    vozrast = CharField()
    data_start = DateField()
    data_end = DateField()
    mesto = CharField(20)
    referee = CharField()
    kat_ref = CharField(10)
    secretary = CharField()
    kat_sek = CharField(10)

    class Meta:
        db_table = "titles"


class Coach(BaseModel):
    coach = CharField()

    class Meta:
        db_table = "coachs"
        order_by = "coach"


class Player(BaseModel):
    num = CharField(10)
    player = CharField(50)
    bday = DateField()
    rank = IntegerField()
    city = CharField()
    region = CharField()
    razryad = CharField(10)
    coach_id = ForeignKeyField(Coach)
    # mesto = IntegerField()

    class Meta:
        db_table = "players"
        order_by = "rank"


class R_list(BaseModel):
    r_number = IntegerField()
    r_list = IntegerField()
    r_fname = CharField(50)
    r_bithday = DateField()
    r_city = CharField(30)

    class Meta:
        db_table = "r_lists"
        order_by = "r_fname"


class R1_list(BaseModel):
    r1_number = IntegerField()
    r1_list = IntegerField()
    r1_fname = CharField(50)
    r1_bithday = DateField()
    r1_city = CharField(30)

    class Meta:
        db_table = "r1_lists"
        order_by = "r1_fname"


class Region(BaseModel):
    region = CharField()

    class Meta:
        db_table = "regions"
        order_by = "region"


class City(BaseModel):
    city = CharField()
    region_id = ForeignKeyField(Region)

    class Meta:
        db_table = "cities"
        order_by = "city"





