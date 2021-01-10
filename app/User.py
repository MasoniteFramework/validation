""" User Model """
try:
    from masoniteorm.models import Model
except:
    from config.database import Model

class User(Model):
    """User Model
    """

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
