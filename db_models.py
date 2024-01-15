from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer)


class Model(Base):
    __tablename__ = "models"
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    price = Column(Integer)


class Data(Base):
    __tablename__ = "data"
    user_id = Column(Integer)
    data_id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(Date)
    ACCESS_ALL_DOWNLOADS = Column(Boolean)
    ACCESS_CACHE_FILESYSTEM = Column(Boolean)
    ACCESS_CHECKIN_PROPERTIES = Column(Boolean)
    ACCESS_COARSE_LOCATION = Column(Boolean)
    ACCESS_COARSE_UPDATES = Column(Boolean)
    ACCESS_LOCATION_EXTRA_COMMANDS = Column(Boolean)
    ACCESS_MTK_MMHW = Column(Boolean)
    ACCESS_NETWORK_STATE = Column(Boolean)
    ACCESS_SUPERUSER = Column(Boolean)
    ACCESS_WIFI_STATE = Column(Boolean)
    AUTHENTICATE_ACCOUNTS = Column(Boolean)
    BATTERY_STATS = Column(Boolean)
    BILLING = Column(Boolean)
    BIND_DEVICE_ADMIN = Column(Boolean)
    BLUETOOTH = Column(Boolean)
    C2D_MESSAGE = Column(Boolean)
    CALL_PHONE = Column(Boolean)
    CAMERA = Column(Boolean)
    CHANGE_NETWORK_STATE = Column(Boolean)
    DISABLE_KEYGUARD = Column(Boolean)
    DOWNLOAD_WITHOUT_0TIFICATION = Column(Boolean)
    GET_ACCOUNTS = Column(Boolean)
    GET_TASKS = Column(Boolean)
    INTERACT_ACROSS_USERS = Column(Boolean)
    INTERNET = Column(Boolean)
    KILL_BACKGROUND_PROCESSES = Column(Boolean)
    MEDIA_BUTTON = Column(Boolean)
    MODIFY_AUDIO_SETTINGS = Column(Boolean)
    MODIFY_PHONE_STATE = Column(Boolean)
    READ_CONTACTS = Column(Boolean)
    READ_EXTERNAL_STORAGE = Column(Boolean)
    READ_LOGS = Column(Boolean)
    READ_OWNER_DATA = Column(Boolean)
    READ_PHONE_STATE = Column(Boolean)
    READ_SETTINGS = Column(Boolean)
    READ_SMS = Column(Boolean)
    RECEIVE_BOOT_COMPLETED = Column(Boolean)
    RECEIVE_SMS = Column(Boolean)
    RECEIVE_USER_PRESENT = Column(Boolean)
    RECORD_AUDIO = Column(Boolean)
    RESTART_PACKAGES = Column(Boolean)
    SDCARD_WRITE = Column(Boolean)
    SEND_SMS = Column(Boolean)
    STORAGE = Column(Boolean)
    SYSTEM_ALERT_WINDOW = Column(Boolean)
    USES_POLICY_FORCE_LOCK = Column(Boolean)
    USE_FINGERPRINT = Column(Boolean)
    VIBRATE = Column(Boolean)
    WAKE_LOCK = Column(Boolean)
    WRITE_EXTERNAL_STORAGE = Column(Boolean)
    WRITE_INTERNAL_STORAGE = Column(Boolean)
    WRITE_MEDIA_STORAGE = Column(Boolean)
    WRITE_OWNER_DATA = Column(Boolean)


class Prediction(Base):
    __tablename__ = "predictions"
    model_id = Column(Integer)
    data_id = Column(Integer)
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_time = Column(Integer)
    answer = Column(Boolean)


class UserHistory(Base):
    __tablename__ = "users_history"
    user_id = Column(Integer)
    prediction_id = Column(Integer)
    user_history_id = Column(Integer, primary_key=True, autoincrement=True)
