from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import asyncio
db = SQLAlchemy()
mail = Mail()

class Profile:
    __images_path = None

    @staticmethod
    def get_images_path():
        home_path = Path(__file__).parent
        images_path = home_path.joinpath('static/images')
        # 确保image存在
        if not images_path.exists():
            images_path.mkdir(parents=True)  # parents=True确保父级文件夹存在
        return images_path
