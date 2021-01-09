""" Providers Configuration File """

from masonite.providers import (
    AppProvider,
    RequestHelpersProvider,
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

from src.masonite.validation.providers import ValidationProvider
from masoniteorm.providers.ORMProvider import ORMProvider

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
    ViewProvider,
    ORMProvider,
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
