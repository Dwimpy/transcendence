from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FortyTwoAccount(ProviderAccount):
    pass


class FortyTwoProvider(OAuth2Provider):
    id = '42'
    name = '42'
    account_class = FortyTwoAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(
            login=data.get('login'),
            first_name=data.get('first_name'),
            email=data.get('email')
        )

    def get_default_scope(self):
        scope = ['public']
        return scope


provider_classes = [FortyTwoProvider]
providers.registry.register(FortyTwoProvider)
