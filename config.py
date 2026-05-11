import urllib.parse

password = urllib.parse.quote_plus("Akrm@123")

class Config:
    SECRET_KEY = "smart-task-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://postgres:{password}@localhost:5432/smart_task_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False