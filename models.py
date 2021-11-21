from peewee import *


db = SqliteDatabase("comp_db.db")


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class Coach(BaseModel):
    coach = CharField()

    class Meta:
        db_table = "coachs"
        order_by = "coach"


class R_list_m(BaseModel):
    r_number = IntegerField()
    r_list = IntegerField()
    r_fname = CharField(50)
    r_bithday = DateField()
    r_city = CharField(30)

    class Meta:
        db_table = "r_lists_m"
        order_by = "r_fname"


class R_list_d(BaseModel):
    r_number = IntegerField()
    r_list = IntegerField()
    r_fname = CharField(50)
    r_bithday = DateField()
    r_city = CharField(30)

    class Meta:
        db_table = "r_lists_d"
        order_by = "r_fname"


class R1_list_m(BaseModel):
    r1_number = IntegerField()
    r1_list = IntegerField()
    r1_fname = CharField(50)
    r1_bithday = DateField()
    r1_city = CharField(30)

    class Meta:
        db_table = "r1_lists_m"
        order_by = "r1_fname"


class R1_list_d(BaseModel):
    r1_number = IntegerField()
    r1_list = IntegerField()
    r1_fname = CharField(50)
    r1_bithday = DateField()
    r1_city = CharField(30)

    class Meta:
        db_table = "r1_lists_d"
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
    gamer = CharField(20)
    full_name_comp = CharField()

    class Meta:
        db_table = "titles"


class Player(BaseModel):
    player = CharField(50)
    bday = DateField()
    rank = IntegerField()
    city = CharField()
    region = CharField()
    razryad = CharField()
    coach_id = ForeignKeyField(Coach)
    mesto = IntegerField(null=True)
    full_name = CharField()
    title_id = ForeignKeyField(Title)

    class Meta:
        db_table = "players"
        order_by = "rank"


class Result(BaseModel):
    system_stage = CharField()
    number_group = CharField()
    tours = CharField()
    player1 = CharField()
    player2 = CharField()
    winner = CharField(null=True)
    points_win = IntegerField(null=True)
    score_in_game = CharField(20, null=True)
    score_win = CharField(null=True)
    loser = CharField(null=True)
    points_loser = IntegerField(null=True)
    score_loser = CharField(null=True)
    title_id = ForeignKeyField(Title)


    class Meta:
        db_table = "results"
        opder_by = "id"


class System(BaseModel):
    title_id = ForeignKeyField(Title)
    total_athletes = IntegerField()
    total_group = IntegerField()
    max_player = IntegerField(null=True)
    stage = CharField()
    page_vid = CharField()
    label_string = CharField()
    kol_game_string = CharField()
    choice_flag = BooleanField()
    score_flag = IntegerField()
    visible_game = BooleanField()

    class Meta:
        db_table = "system"


class Game_list(BaseModel):
    number_group = CharField()
    rank_num_player = IntegerField()
    player_group = ForeignKeyField(Player)
    system_id = ForeignKeyField(System)

    class Meta:
        db_table = "game_lists"
        order_by = "number_group"


class Tour(BaseModel):
    person_in_group = CharField()
    table_1 = CharField(10)
    table_2 = CharField(10)
    table_3 = CharField(10)
    table_4 = CharField(10)
    table_5 = CharField(10)
    table_6 = CharField(10)
    table_7 = CharField(10)
    table_8 = CharField(10)
    result_id = ForeignKeyField(Result)

    class Meta:
        db_table = "tours"
        order_by = "person_in_group"


class Choice(BaseModel):
    player_choice = ForeignKeyField(Player)
    family = CharField()
    region = CharField()
    coach = CharField()
    rank = IntegerField()
    basic = CharField(null=True)
    group = CharField(null=True)
    posev_group = IntegerField(null=True)
    mesto_group = IntegerField(null=True)
    semi_final = IntegerField(null=True)
    n_group = CharField(null=True)
    posev_sf = IntegerField(null=True)
    mesto_semi_final = IntegerField(null=True)
    final = CharField(null=True)
    posev_final = IntegerField(null=True)
    mesto_final = IntegerField(null=True)
    super_final = CharField(null=True)
    title_id = ForeignKeyField(Title)

    class Meta:
        db_table = "choices"


class Delete_player(BaseModel):
    player_del = ForeignKeyField(Player)
    player = CharField()
    bday = DateField()
    rank = IntegerField()
    city = CharField()
    region = CharField()
    razryad = CharField(10)
    coach_id = ForeignKeyField(Coach)

    class Meta:
        db_table = "delete_players"



