'''
agents
======

The following methods allow for interaction into the Nessus Manager 
`agents <https://localhost:8834/api#/resources/agents>`_ 
API endpoints.

Methods available on ``nessus.agents``:

.. rst-class:: hide-signature
.. autoclass:: AgentsAPI

    .. automethod:: details
    .. automethod:: list
    .. automethod:: unlink

'''
from .base import NessusEndpoint


class AgentsAPI(NessusEndpoint):
    def list(self):
        '''
        Get the listing of configured agents from Nessus Manager

        `agents: list <https://localhost:8834/api#/resources/agents/list>`_

        Args:
            None:

        Returns:
            list: 
                Returns a list of Agent resources

        Examples:
            Getting the listing of all agents:

            >>> agents = nessus.agents.list()
        '''
        agents = self._api.get('agents').json()
        return agents['agents']

    def delete(self, *agent_ids):
        '''
        Delete an agent

        `agents: get <https://localhost:8834/api#/resources/agents/delete>`_

        Args:
            agent_ids (list): 
                The identifier of the agent.

        Returns:
            None:

        Examples:

            >>> nessus.agents.delete(1)


            >>> nessus.agents.delete(1, 2, 4)

        '''
        if (len(agent_ids) == 1):
            self._api.delete('agents/{}'.format(agent_ids[0]))
        else:
            self._api.delete(
                'agents', json={'ids': [self._check('agent_ids', i, int) for i in agent_ids]})

    def unlink(self, *agent_ids):
        '''
        Unlink one or multiple agents from the Nessus Manager.

        `agents: delete <https://localhost:8834/api#/resources/agents/unlink>`_

        Args:
            *agent_ids (list)(int):
                The ID of the agent to delete

        Returns:
            None: A singular agent was successfully unlinked.

        Examples:
            Unlink a singular agent:

            >>> tio.agents.unlink(1)

            Unlink many agents:

            >>> tio.agents.unlink(1, 2, 3)
        '''

        if len(agent_ids) <= 1:
            # as only a singular agent_id was sent over, we can call the delete
            # API
            self._api.delete('agents/{}/unlink'.format(
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            return self._api.delete('agents/unlink'.format(
                self._check('scanner_id', scanner_id, int)),
                json={'ids': [self._check('agent_ids', i, int) for i in agent_ids]}).json()
