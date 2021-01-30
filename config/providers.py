""" Providers Configuration File """

from masonite.providers import (
    AppProvider,
    AuthenticationProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    WhitenoiseProvider,
    MailProvider,
    UploadProvider,
    ViewProvider,
    HelpersProvider,
    QueueProvider,
    BroadcastProvider,
    CacheProvider,
    CsrfProvider,
)
from masonite.providers import RequestHelpersProvider
from masoniteorm.providers.ORMProvider import ORMProvider

from src.masonite.validation.providers import ValidationProvider

"""
|--------------------------------------------------------------------------
| Providers List
|--------------------------------------------------------------------------
|
| Providers are a simple way to remove or add functionality for Masonite
| The providers in this list are either ran on server start or when a
| request is made depending on the provider. Take some time to learn
| more about Service Providers in our documentation
|
"""


PROVIDERS = [
    # Framework Providers
    AppProvider,
    RequestHelpersProvider,
    CsrfProvider,
    AuthenticationProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    # WhitenoiseProvider,
    ORMProvider,
    ViewProvider,
    ValidationProvider,

    # Optional Framework Providers
    # MailProvider,
    # UploadProvider,
    # QueueProvider,
    # CacheProvider,
    # BroadcastProvider,
    # CacheProvider,
    # HelpersProvider,

    # Third Party Providers

    # Application Providers

]
