"""A Validation Service Provider."""

from masonite.provider import ServiceProvider
from .. import Validator, ValidationFactory
from ..commands.RuleEnclosureCommand import RuleEnclosureCommand
from ..commands.RuleCommand import RuleCommand

class ValidationProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.singleton('Validator', Validator)
        self.app.bind('RuleEnclosureCommand', RuleEnclosureCommand())
        self.app.bind('RuleCommand', RuleCommand())

    def boot(self, validator: Validator):
        validator.extend(ValidationFactory().registry)
