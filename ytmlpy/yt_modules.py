
from sqlalchemy import (
    create_engine, Column, ForeignKey, Integer, Float, String,
    Date, DateTime
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, reconstructor, relationship
from sqlalchemy.ext.serializer import loads, dumps
from datetime import datetime
# import pytz
from contextlib import contextmanager
from sqlalchemy.sql import func

# Base = declarative_base()
# dbname = 'ytml'
# url = 'mysql+pymysql://kamirazio:g019116@localhost/%s?charset=utf8' % dbname
# engine = create_engine(url, echo = False)
# Session = sessionmaker(bind=engine)

print('what time?')
print(datetime.now())
# tokyo_timezone = pytz.timezone('Asia/Tokyo')
# tokyo_datetime = tokyo_timezone.localize(now)
# print(f'Asia/Tokyo {tokyo_datetime}')


#モデル定義
#モデルとDBのテーブルが一対一の関係になる。
#モデルのフィールドに対応した、カラムがテーブルに追加

#モデル定義 : このクラスを継承し -> Videoモデルを定義
Base = declarative_base()

class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lemma = Column(String, index=True)
    word = Column(String)
    user_id = Column(String, index=True)
    uid = Column(String, index=True)
    tid = Column(String)
    # video_id = Column(String)
    q_num = Column(Integer)
    order = Column(Integer)
    # mode = Column(String)
    jacet = Column(Integer)
    status = Column(Integer)
    mark = Column(Integer)

    t_dict = Column(Integer)
    t_save = Column(Integer)
    # t_complete = Column(Integer)
    # t_experience = Column(Integer)
    t_success = Column(Integer)
    t_repeat = Column(Integer)
    t_miss = Column(Integer)
    t_cheat = Column(Integer)
    t_skip = Column(Integer)
    created = Column(DateTime(timezone=False), default=func.now())

    def __repr__(self):
        return "<Words class>"


class Ejdic(Base):
    __tablename__ = 'ejdic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    en = Column(String, index=True)
    ja = Column(String, index=True)

    def __repr__(self):
        return "<Ejdic class>"

class Jacet(Base):
    __tablename__ = 'jacet'
    rank = Column(Integer, primary_key=True)
    en = Column(String, index=True)
    tag = Column(String, index=True)

    def __repr__(self):
        return "<Jacet class>"

# class Classrooms(Base):
#     __tablename__ = 'classrooms'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     uuid = Column(String, index=True)
#     status = Column(Integer, index=True)
#
#     uid = Column(String,index=True)
#     role = Column(Integer)
#
#     title = Column(String)
#     memo = Column(String)
#     task_ids = Column(String)
#     tags = Column(String)
#
#     created = Column(DateTime(timezone=False), default=func.now())
#     modified = Column(DateTime(timezone=False), default=func.now())
#
#     def __repr__(self):
#         return "<Classrooms class>"


# class Tasksets(Base):
#     __tablename__ = 'tasksets'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     classroom_id = Column(String,index=True)
#     tid = Column(String)
#     status = Column(Integer, index=True)
#     user_id = Column(String)
#     uid = Column(String)
#     created = Column(DateTime(timezone=False), default=func.now())
#     modified = Column(DateTime(timezone=False), default=func.now())
#
#     def __repr__(self):
#         return "<Tasksets class>"


# class Games(Base):
#     __tablename__ = 'games'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     task_id = Column(String, index=True)
#     tid = Column(String, index=True)
#     video_id = Column(String, index=True)
#     # user_id = Column(String)
#     # mode = Column(String)
#
#     q_num = Column(Integer, index=True)
#     done = Column(Integer)
#     fullmarks = Column(Integer)
#     score = Column(Integer)
#
#     completed = Column(String)
#     fail_list = Column(String)
#     fine_list = Column(String)
#     success_list = Column(String)
#     comment = Column(String)
#
#     created = Column(DateTime(timezone=False), default=func.now())
#     # modified = Column(DateTime, default=datetime.now, nullable=False)
#
#
#     def __repr__(self):
#         return "<Games class>"

class Scripts(Base):
    __tablename__ = 'scripts_ex'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # uuid = Column(String, index=True)
    tid = Column(String, index=True)
    vid = Column(String, index=True)
    video_id = Column(String, index=True)

    q_num = Column(Integer, index=True)
    timestamp = Column(String)
    script_main = Column(String)
    script_local = Column(String)

    user_level = Column(Integer)
    user_level2 = Column(Integer)
    question = Column(String)
    question2 = Column(String)
    probability = Column(String)
    probability2 = Column(String)
    blank_rate = Column(Integer)
    blank_rate2 = Column(Integer)

    token = Column(String)
    stopword = Column(String)
    tagged = Column(String)
    tag_id = Column(String)
    lemma = Column(String)
    jacet = Column(String)

    comment = Column(String)
    advice = Column(String)
    done = Column(Integer, index=True)
    created = Column(DateTime(timezone=False), default=func.now())
    modified = Column(DateTime(timezone=False), default=func.now())


    def __repr__(self):
        return "<Scripts class>"


class Tasks(Base):
    __tablename__ = 'tasks_ex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, index=True)
    video_id = Column(String, index=True)
    video_key = Column(String, index=True)
    vid = Column(Integer, index=True)
    lang = Column(String, index=True)
    local_lang = Column(String)
    host = Column(String)

    status = Column(Integer)
    memo = Column(String)

    mode = Column(String)
    chunk = Column(Integer)
    level = Column(Integer)
    blank_rate = Column(Integer)
    score = Column(Integer)
    progress = Column(Integer)

    user_id = Column(String)
    uid = Column(String)

    owner_id = Column(String)
    follow_id = Column(String)
    origin = Column(String)

    vol = Column(Integer) #need?
    start_q = Column(Integer) #need?
    end_q = Column(Integer) #need?
    total_q = Column(Integer) #need?

    v_relate = Column(Integer)
    v_enjoy = Column(Integer)
    v_play = Column(Integer)
    v_understand= Column(Integer)
    comment = Column(String)
    created = Column(DateTime(timezone=False), default=func.now())
    modified = Column(DateTime(timezone=False), default=func.now())

    def __repr__(self):
        return "<Tasks class>"


class Videos(Base):
    __tablename__ = 'videos_ex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, index=True)
    video_id = Column(String, index=True)
    video_key = Column(String, index=True)
    host = Column(String)
    lang = Column(String, index=True)
    video_lang = Column(String)
    lang_list = Column(String)
    url = Column(String)
    title = Column(String)
    plot = Column(String)
    subtitle = Column(String)
    plot_id = Column(String)
    description = Column(String)
    memo = Column(String)
    img = Column(String)
    video_date = Column(DateTime(timezone=False), default=func.now())
    channel = Column(String)
    channel_id = Column(String)
    author = Column(String)
    author_id = Column(String)
    video_link = Column(String)
    duration = Column(Integer)
    adjustment = Column(Float)

    size = Column(String)
    difficulty1 = Column(String)
    difficulty2 = Column(String)

    keywords = Column(String)
    tags = Column(String)
    rating = Column(String)
    viewed = Column(Integer)
    created = Column(DateTime(timezone=False), default=func.now())
    modified = Column(DateTime(timezone=False), default=func.now())

    def __repr__(self):
        return "<Videos class>"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, index=True)
    username = Column(String)
    email = Column(String, index=True)
    password = Column(String)
    local_lang = Column(String)
    school = Column(String)
    grade = Column(String)
    affiliation = Column(String)
    student_id = Column(String)
    created = Column(DateTime(timezone=False), default=func.now())
    modified = Column(DateTime(timezone=False), default=func.now())

    def __repr__(self):
        return "<Users class>"

@contextmanager
def start_session(commit=False):

    """セッションを開始します。
    Args:
        commit: Trueにするとセッション終了時にcommitします。
    Yields:
        SqlAlcyemyのセッション
    Usage:
        with start_session() as session:
            q = session.query(Table)...
    """

    session = None
    try:
        # トランザクションを開始します。
        # ※autocommit=Falseなので、自動的にトランザクションが開始されます。
        session = Session()
        try:
            yield session
            if commit:
                session.commit()
        except:
            # 例外発生時はトランザクションをロールバックして、その例外をそのまま投げます。
            session.rollback()
            raise
    finally:
        if session is not None:
            session.close()


class DynamicTableMixin(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def stock_id(cls):
        return Column(Integer, ForeignKey('stock.id'))
