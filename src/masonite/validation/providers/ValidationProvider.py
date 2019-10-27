"""A Validation Service Provider."""

from masonite.provider import ServiceProvider
from masonite.view import View
from .. import Validator, ValidationFactory, MessageBag
from ..commands.RuleEnclosureCommand import RuleEnclosureCommand
from ..commands.RuleCommand import RuleCommand

class ValidationProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.singleton('Validator', Validator)
        self.app.bind('RuleEnclosureCommand', RuleEnclosureCommand())
        self.app.bind('RuleCommand', RuleCommand())

    def boot(self, validator: Validator, view: View):
        validator.extend(ValidationFactory().registry)

        view.share({
            'bag': MessageBag
        })

