## -*- coding: utf-8 -*-
from pprint import pprint
import time
from oauth_provider.models import Resource
from oauth_provider.tests.auth import BaseOAuthTestCase

class OAuthTestOauthRequiredDecorator(BaseOAuthTestCase):
    def setUp(self):
        # create Resource 'all' for all requests without scope specified
        Resource.objects.create(name="all")
        super(OAuthTestOauthRequiredDecorator, self).setUp()

    def _oauth_signed_get(self, url):
        parameters = {
            'oauth_consumer_key': self.CONSUMER_KEY,
            'oauth_signature_method': "PLAINTEXT",
            'oauth_version': "1.0",
            'oauth_token': self.ACCESS_TOKEN_KEY,
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': str(int(time.time()))+"nonce",
            'oauth_signature': "%s&%s" % (self.CONSUMER_SECRET, self.ACCESS_TOKEN_SECRET),
            "additional_data": "whoop" # some additional data
            }
        response = self.c.get(url, parameters)
        return response

    def test_resource_some_scope_view_authorized(self):
        """Tests view that was created using @oauth_required("some") decorator
        """
        #ensure there is a Resource object for this scope
        self.resource = Resource.objects.create(name="some")
        #set scope for requested token
        self.request_token_parameters['scope'] = self.resource.name

        self._request_token()
        self._authorize()

        response = self._oauth_signed_get("/oauth/some/")
        self.assertEqual(response.status_code, 200)

    def test_resource_some_scope_view_not_authorized(self):
        """Tests that view created with @oauth_required("some") decorator won't give access
        when requested using token with different scope
        """
        #set scope to 'all', notice that view we test is hidden behind 'some' scope
        self.request_token_parameters['scope'] = "all"
        self._request_token()
        self._authorize()

        response = self._oauth_signed_get("/oauth/some/")
        self.assertEqual(response.status_code, 401)

    def test_resource_None_view(self):
        """Tests that view created using @oauth_required decorator gives access when requested
        using token without scope specified
        """
        #request token without setting scope
        self.request_token_parameters.pop('scope')
        self._request_token()
        self._authorize()

        response = self._oauth_signed_get("/oauth/none/")
        self.assertEqual(response.status_code, 200)

    def test_resource_None_scope_view_not_authorized(self):
        """Tests that view created with @oauth_required decorator won't give access
        when requested using token with scope!="all"
        """
        #ensure there is a Resource object for this scope
        self.resource = Resource.objects.create(name="some_new_scope")
        #set scope to 'all', notice that view we test is hidden behind 'some' scope
        self.request_token_parameters['scope'] = self.resource.name
        self._request_token()
        self._authorize()

        response = self._oauth_signed_get("/oauth/some/")
        self.assertEqual(response.status_code, 401)