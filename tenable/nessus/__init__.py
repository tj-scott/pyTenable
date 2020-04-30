'''
.. autoclass:: Nessus

.. automodule:: tenable.nessus.agent_groups
.. automodule:: tenable.nessus.folders
.. automodule:: tenable.nessus.scans

Raw HTTP Calls
==============

Even though the ``Nessus`` object pythonizes the Nessus Manager API for you,
there may still be the occasional need to make raw HTTP calls to the IO API.
The methods listed below aren't run through any naturalization by the library
aside from the response code checking.  These methods effectively route
directly into the requests session.  The responses will be Response objects from
the ``requests`` library.  In all cases, the path is appended to the base
``url`` paramater that the ``Nessus`` object was instantiated with.

Example:

.. code-block:: python

   resp = nessus.get('scans')

.. py:module:: tenable.nessus
.. rst-class:: hide-signature
.. py:class:: Nessus

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
import logging
from tenable.base import APISession
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .editor import EditorAPI
from .folders import FoldersAPI
from .scans import ScansAPI


class Nessus(APISession):
    '''
    The Tenable.io object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Nessus Manager
        secret_key (str):
            The user's API secret key for Nessus Manager
        url (str, optional):
            The base URL that the paths will be appended onto. default URL is
            ``https://localhost:8834/``
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        ua_identity (str, optional):
            An application identifier to be added into the User-Agent string
            for the purposes of application identification.

    Examples:
        >>> from tenable.nessus import Nessus
        >>> nessus = Nessus('ACCESS_KEY', 'SECRET_KEY')
    '''

    _tzcache = None
    _url = 'https://localhost:8834'

    @property
    def agent_groups(self):
        return AgentGroupsAPI(self)

    @property
    def agents(self):
        return AgentsAPI(self)

    @property
    def editor(self):
        return EditorAPI(self)

    @property
    def folders(self):
        return FoldersAPI(self)

    @property
    def scans(self):
        return ScansAPI(self)

    @property
    def _tz(self):
        '''
        As we will be using the timezone listing in a lot of parameter checking,
        we should probably cache the response as a private attribute to speed
        up checking times.
        '''
        if not self._tzcache:
            self._tzcache = self.scans.timezones()
        return self._tzcache

    def __init__(self, access_key, secret_key, url, retries=None,
                 backoff=None, ua_identity=None, session=None, verify=True):
        self._access_key = access_key
        self._secret_key = secret_key
        self._verify = verify
        APISession.__init__(self, url, retries, backoff, ua_identity, session)

    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
        '''
        Add SSL Verification flag
        '''
        self._session.verify = self._verify
