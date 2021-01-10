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
try:
    from masonite.providers import RequestHelpersProvider
    from masoniteorm.providers.ORMProvider import ORMProvider
    has_orm = True
except:
    has_orm = False

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
    CsrfProvider,
    AuthenticationProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    # WhitenoiseProvider,
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

if has_orm:
    PROVIDERS.insert(1, RequestHelpersProvider)
    PROVIDERS.insert(len(PROVIDERS)-2, ORMProvider)