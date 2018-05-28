from django.contrib.auth.apps import AuthConfig as ContribAuthConfig

class AuthConfig(ContribAuthConfig):
    verbose_name = 'Groups'
