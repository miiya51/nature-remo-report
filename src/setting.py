import datetime
import os
from functools import wraps
import logging

from remo import NatureRemoAPI
from sqlalchemy import Column, create_engine
from sqlalchemy.dialects.mysql import NUMERIC, TIMESTAMP, VARCHAR
from sqlalchemy.orm import declarative_base
import sys

# ハンドラーをLoggerに追加
# logging.addHandler(fh)

Base = declarative_base()
#コンテナの環境変数から設定の読み取り
API_KEY: str = os.environ.get("remo_token")
DB_USER: str = os.environ.get("db_user")
DB_PASSWORD: str = os.environ.get("db_password")
DB_SERVER: str = os.environ.get("db_server")
DB_NAME: str = os.environ.get("db_name")
INTERVAL_MINUTES: int = int(os.environ.get("interval_time"))

api = NatureRemoAPI(API_KEY)
tz_jst_name = datetime.timezone(datetime.timedelta(hours=9), name="JST")
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}")

#　テーブルクラスの定義
class NATURE_REMO(Base):
    __tablename__ = "nature_remo"
    id = Column(VARCHAR(36), primary_key=True)
    get_time = Column(TIMESTAMP, primary_key=True)
    device_name = Column(VARCHAR(36))
    temp = Column(NUMERIC(2, 1))

# loggerの定義
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 標準出力へのハンドラーを作成
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# フォーマットを設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def my_log(logger):
    def decorator_fn(fn):
        @wraps(fn)
        def wrap_fn(*args, **kwargs):
            #local_args = locals()
            logger.debug(f"{fn.__name__} WAS CALLED")
            return_val = fn(*args, **kwargs)
            logger.debug(f"{fn.__name__} FINISHED")
            return return_val

        return wrap_fn

    return decorator_fn

