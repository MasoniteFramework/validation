"""A Validation Service Provider."""

from masonite.provider import ServiceProvider
from masonite.view import View
from .. import Validator, ValidationFactory, MessageBag
from ..commands.RuleEnclosureCommand import RuleEnclosureCommand
from ..commands.RuleCommand import RuleCommand


class ValidationProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.singleton("Validator", Validator)
        self.app.bind("RuleEnclosureCommand", RuleEnclosureCommand())
        self.app.bind("RuleCommand", RuleCommand())

    def boot(self, validator: Validator, view: View):
        validator.extend(ValidationFactory().registry)

        MessageBag.get_errors = self._get_errors

        view.share({"bag": MessageBag.view_helper})

    def _get_errors(self):
        request = self.app.make('Request')
        messages = []
        for error, message in request.session.get_flashed_messages().get('errors', {}).items():
            messages += message

        return messages
