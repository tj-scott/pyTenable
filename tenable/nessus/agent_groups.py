'''
agent_groups
============

The following methods allow for interaction into the Tenable.io
`agent groups <https://{nessus manager}]/api#/resources/agent-groups>`_
API endpoints.

Methods available on ``nessus.agent_groups``:

.. rst-class:: hide-signature
.. autoclass:: AgentGroupsAPI

    .. automethod:: add_agent
    .. automethod:: configure
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: delete_agent
    .. automethod:: details
    .. automethod:: list
'''
from .base import NessusEndpoint


class AgentGroupsAPI(NessusEndpoint):
    def add_agent(self, group_id, *agent_ids):
        '''
        Adds an agent or multiple agents to the agent group specified.

        #/resources/agent-groups/add-agent>`_
        `agent-groups: add-agent <https://{nessus manager}/api
        #/resources/agent-groups/add-agents>`_
        `agent-groups: add-agent <https://{nessus manager}/api

        Args:
            group_id (int): The id of the group
            *agent_ids (int): The id of the agent

        Returns:
            None: Single Agent added successfully
            dict: Task resource if multiple Agents were added.

        Examples:
            Adding a singular agent:

            >>> nessus.agent_groups.add_agent(1, 1)

            Adding multiple agents:

            >>> nessus.agent_groups.add_agent(1, 1, 2, 3)
        '''

        if len(agent_ids) <= 1:
            # if there is only 1 agent id, we will perform a singular add.
            self._api.put('agent-groups/{}/agents/{}'.format(
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            # If there are many agent_ids, then we will want to perform a bulk
            # operation.
            self._api.put(
                'agent-groups/{}/agents'.format(
                    self._check('group_id', group_id, int)),
                json={'ids': [self._check('agent_id', i, int) for i in agent_ids]})

    def configure(self, group_id, name):
        '''
        Renames an existing agent group.

        #/resources/agent-groups/configure>`_
        `agent-groups: configure <https://{nessus manager}/api

        Args:
            group_id (int): The id of the group
            name (str): The new name for the agent group

        Returns:
            None: Agent group updated successfully

        Examples:
            >>> nessus.agent_groups.configure(1, 'New Name')
        '''
        self._api.put('agent-groups/{}'.format(
            self._check('group_id', group_id, int)
        ), json={'name': self._check('name', name, str)}).json()

    def create(self, name):
        '''
        Creates a new agent group.

        #/resources/agent-groups/create>`_
        `agent-groups: create <https://{nessus manager}/api

        Args:
            name (str): The name of the agent group

        Returns:
            dict:
                The dictionary object representing the newly minted agent group

        Examples:
            >>> group = nessus.agent_groups.create('New Agent Group')
        '''
        return self._api.post(
            'agent-groups'.format(
            ), json={'name': self. _check('name', name, str)}).json()

    def delete(self, *group_ids):
        '''
        Delete an agent group.

        #/resources/agent-groups/delete-group>`_
        `agent-groups: delete <https://{nessus manager}/api
        #/resources/agent-groups/delete-groups>`_
        `agent-groups: delete <https://{nessus manager}/api

        Args:
            *group_ids (int): The id of the agent group to delete

        Returns:
            None: A singular agent was deleted from the group successfully.

        Examples:
            >>> nessus.agent_groups.delete(1)

        Examples:
            Deleting a singular agent group:

            >>> nessus.agent_groups.delete(1)

            Deleting Multiple agent groups:

            >>> nessus.agent_groups.delete(1, 2, 3)
        '''
        if len(group_ids) <= 1:
            # if there is only 1 group id, we will perform a singular delete.
            return self._api.delete('agent-groups/{}'.format(
                self._check('group_id', group_ids[0], int)
            ))
        else:
            # Multiple group id's, perform a bulk delete
            return self._api.delete('agent-groups',
                                    json={'ids': [self._check('group_id', i, int) for i in group_ids]})

    def delete_agent(self, group_id, *agent_ids):
        '''
        Delete one or many agents from an agent group.

        #/resources/agent-groups/delete-agent>`_
        `agent-groups: delete-agent <https://{nessus manager}/api
        #/resources/agent-groups/delete-agents>`_
        `agent-groups: delete-agent <https://{nessus manager}/api

        Args:
            group_id (int): The id of the agent group to remove the agent from
            *agent_ids (int): The id of the agent to be removed

        Returns:
            None: A singular agent was deleted from the group successfully.

        Examples:
            Delete a singular agent from an agent group:

            >>> nessus.agent_groups.delete_agent(1, 1)

            Delete multiple agents from an agent group:

            >>> nessus.agent_groups.delete_agent(1, 1, 2, 3)
        '''

        if len(agent_ids) <= 1:
            # if only a singular agent_id was passed, then we will want to
            self._api.delete('agent-groups/{}/agents/{}'.format(
                self._check('group_id', group_id, int),
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            # if multiple agent ids were requested to be deleted, then we will
            # call the bulk deletion API.
            self._api.delete('agent-groups/{}/agents/'.format(
                self._check('group_id', group_id, int)),
                json={'ids': [self._check('agent_ids', i, int) for i in agent_ids]})

    def details(self, group_id):
        '''
        Retrieve the details about the specified agent group.

        #/resources/agent-groups/details>`_
        `agent-groups: details <https://{nessus manager}/api

        Args:
            group_id (int): The id of the agent group to remove the agent from

        Returns:
            dict:
                The dictionary object representing the requested agent group

        Examples:
            >>> group = nessus.agent_groups.details(1)
            >>> pprint(group)
        '''
        return self._api.get(
            'agent-groups/{}'.format(
                self._check('group_id', group_id, int)
            )).json()

    def list(self):
        '''
        Returns a list of agent groups

        #/resources/agent-groups/list>`_
        `agent-groups: details <https://{nessus manager}/api

        Args:
            None: This request does not have any parameters.

        Returns:
            list: A list of group resource records

        Example:

            >>> groups = nessus.agent_groups.list()
            >>> pprint(groups)
        '''
        return self._api.get('agent-groups').json()["groups"]
