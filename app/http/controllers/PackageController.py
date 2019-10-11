""" Welcome The User To Masonite """

from masonite.view import View
from masonite.request import Request
from app.User import User
from src.masonite.validation.decorators import validate
from src.masonite.validation import required

class PackageController:
    """Controller For Welcoming The User
    """

    def show(self, view: View, request: Request):

        return 'Hello World'

    @validate(required('name'))
    def validate(self):
        return 'success'