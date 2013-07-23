from urllib import urlencode

import oauth2 as oauth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.core.urlresolvers import get_callable

from decorators import oauth_required
from forms import AuthorizeRequestTokenForm
from oauth_provider.compat import UnsafeRedirect
from store import store, InvalidConsumerError, InvalidTokenError
from utils import verify_oauth_request, get_oauth_request, require_params, send_oauth_error
from utils import is_xauth_request, verify_xauth_request
from consts import OUT_OF_BAND

OAUTH_AUTHORIZE_VIEW = 'OAUTH_AUTHORIZE_VIEW'
OAUTH_CALLBACK_VIEW = 'OAUTH_CALLBACK_VIEW'
INVALID_PARAMS_RESPONSE = send_oauth_error(oauth.Error(
                                            _('Invalid request parameters.')))

UNSAFE_REDIRECTS = getattr(settings, "OAUTH_UNSAFE_REDIRECTS", False)

@csrf_exempt
def request_token(request):
    oauth_request = get_oauth_request(request)
    if oauth_request is None:
        return INVALID_PARAMS_RESPONSE

    missing_params = require_params(oauth_request, ('oauth_callback',))
    if missing_params is not None:
        return missing_params

    if is_xauth_request(oauth_request):
        return HttpResponseBadRequest('xAuth not allowed for this method.')

    try:
        consumer = store.get_consumer(request, oauth_request, oauth_request['oauth_consumer_key'])
    except InvalidConsumerError:
        return HttpResponseBadRequest('Invalid Consumer.')

    if not verify_oauth_request(request, oauth_request, consumer):
        return HttpResponseBadRequest('Could not verify OAuth request.')

    try:
        request_token = store.create_request_token(request, oauth_request, consumer, oauth_request['oauth_callback'])
    except oauth.Error, err:
        return send_oauth_error(err)

    ret = urlencode({
        'oauth_token': request_token.key,
        'oauth_token_secret': request_token.secret,
        'oauth_callback_confirmed': 'true'
    })
    return HttpResponse(ret, content_type='application/x-www-form-urlencoded')


@login_required
def user_authorization(request, form_class=AuthorizeRequestTokenForm):
    if 'oauth_token' not in request.REQUEST:
        return HttpResponseBadRequest('No request token specified.')

    oauth_request = get_oauth_request(request)

    try:
        request_token = store.get_request_token(request, oauth_request, request.REQUEST['oauth_token'])
    except InvalidTokenError:
        return HttpResponseBadRequest('Invalid request token.')

    consumer = store.get_consumer_for_request_token(request, oauth_request, request_token)

    if request.method == 'POST':
        form = form_class(request.POST)
        if request.session.get('oauth', '') == request_token.key and form.is_valid():
            request.session['oauth'] = ''
            if form.cleaned_data['authorize_access']:
                request_token = store.authorize_request_token(request, oauth_request, request_token)
                args = { 'oauth_token': request_token.key }
            else:
                args = { 'error': _('Access not granted by user.') }
            if request_token.callback is not None and request_token.callback != OUT_OF_BAND:
                callback_url = request_token.get_callback_url(args)
                if UNSAFE_REDIRECTS:
                    response = UnsafeRedirect(callback_url)
                else:
                    response = HttpResponseRedirect(callback_url)
            else:
                # try to get custom callback view
                callback_view_str = getattr(settings, OAUTH_CALLBACK_VIEW,
                                    'oauth_provider.views.fake_callback_view')
                try:
                    view_callable = get_callable(callback_view_str)
                except AttributeError:
                    raise Exception, "%s view doesn't exist." % callback_view_str

                # try to treat it as Class Based View (CBV)
                try:
                    callback_view = view_callable.as_view()
                except AttributeError:
                    # if it appears not to be CBV treat it like FBV
                    callback_view = view_callable
                
                response = callback_view(request, **args)
        else:
            response = send_oauth_error(oauth.Error(_('Action not allowed.')))
    else:
        # try to get custom authorize view
        authorize_view_str = getattr(settings, OAUTH_AUTHORIZE_VIEW, 
                                    'oauth_provider.views.fake_authorize_view')
        try:
            view_callable = get_callable(authorize_view_str)
        except AttributeError:
            raise Exception, "%s view doesn't exist." % authorize_view_str

        # try to treat it as Class Based View (CBV)
        try:
            authorize_view = view_callable.as_view()
        except AttributeError:
            # if it appears not to be CBV treat it like FBV
            authorize_view = view_callable

        params = oauth_request.get_normalized_parameters()
        # set the oauth flag
        request.session['oauth'] = request_token.key
        response = authorize_view(request, request_token, request_token.get_callback_url(), params)
        
    return response

@csrf_exempt
def access_token(request):
    oauth_request = get_oauth_request(request)
    if oauth_request is None:
        return INVALID_PARAMS_RESPONSE

    # Consumer
    try:
        consumer = store.get_consumer(request, oauth_request, oauth_request['oauth_consumer_key'])
    except InvalidConsumerError:
        return HttpResponseBadRequest('Invalid consumer.')

    is_xauth = is_xauth_request(oauth_request)

    if not is_xauth:

        # Check Parameters
        missing_params = require_params(oauth_request, ('oauth_token', 'oauth_verifier'))
        if missing_params is not None:
            return missing_params

        # Check Request Token
        try:
            request_token = store.get_request_token(request, oauth_request, oauth_request['oauth_token'])
        except InvalidTokenError:
            return HttpResponseBadRequest('Invalid request token.')
        if not request_token.is_approved:
            return HttpResponseBadRequest('Request Token not approved by the user.')

        # Verify Signature
        if not verify_oauth_request(request, oauth_request, consumer, request_token):
            return HttpResponseBadRequest('Could not verify OAuth request.')
       
        # Check Verifier
        if oauth_request.get('oauth_verifier', None) != request_token.verifier:
            return HttpResponseBadRequest('Invalid OAuth verifier.')

    else: # xAuth

        # Check Parameters
        missing_params = require_params(oauth_request, ('x_auth_username', 'x_auth_password', 'x_auth_mode'))
        if missing_params is not None:
            return missing_params

        # Check if Consumer allows xAuth
        if not consumer.xauth_allowed:
            return HttpResponseBadRequest('xAuth not allowed for this method')

        # Check Signature
        if not verify_oauth_request(request, oauth_request, consumer):
            return HttpResponseBadRequest('Could not verify xAuth request.')
        
        # Check Username/Password 
        if is_xauth and not verify_xauth_request(request, oauth_request):
            return HttpResponseBadRequest('xAuth username or password is not valid')
        
        # Handle Request Token
        try:
            #request_token = store.create_request_token(request, oauth_request, consumer, oauth_request.get('oauth_callback'))
            request_token = store.create_request_token(request, oauth_request, consumer, OUT_OF_BAND)
            request_token = store.authorize_request_token(request, oauth_request, request_token)
        except oauth.Error, err:
            return send_oauth_error(err)

    access_token = store.create_access_token(request, oauth_request, consumer, request_token)

    ret = urlencode({
        'oauth_token': access_token.key,
        'oauth_token_secret': access_token.secret
    })
    return HttpResponse(ret, content_type='application/x-www-form-urlencoded')

@oauth_required
def protected_resource_example(request):
    """
    Test view for accessing a Protected Resource.
    """
    return HttpResponse('Protected Resource access!')

@login_required
def fake_authorize_view(request, token, callback, params):
    """
    Fake view for tests. It must return an ``HttpResponse``.
    
    You need to define your own in ``settings.OAUTH_AUTHORIZE_VIEW``.
    """
    return HttpResponse('Fake authorize view for %s with params: %s.' % (token.consumer.name, params))

def fake_callback_view(request, **args):
    """
    Fake view for tests. It must return an ``HttpResponse``.
    
    You can define your own in ``settings.OAUTH_CALLBACK_VIEW``.
    """
    return HttpResponse('Fake callback view.')
