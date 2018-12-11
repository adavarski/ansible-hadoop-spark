#!/usr/bin/python
# coding: utf-8
__version__ = '1.1'
__all__ = [
  '_localcall'
]

import getpass

from ansible.plugins.connection.local import Connection as LocalConnection

class Switch2Local:
    def __init__(self, task, play_context, action_module):
        self._task = task
        self._play_context = play_context
        self._action_module = action_module

        old = dict()
        self._cache = old

        old['t_become'] = task.become
        old['t_become_flags'] = task.become_flags
        old['t_become_method'] = task.become_method
        old['t_become_user'] = task.become_user
        old['t_delegate_to'] = task.delegate_to

        old['pc_become'] = play_context.become
        old['pc_become_flags'] = play_context.become_flags
        old['pc_become_method'] = play_context.become_method
        old['pc_become_user'] = play_context.become_user
        old['pc_connection'] = play_context.connection # -> local
        old['pc_remote_addr'] = play_context.remote_addr # -> localhost
        old['pc_remote_user'] = play_context.remote_user # -> current-user

        old['_connection'] = action_module._connection # -> local-connection

    def turn_on(self):
        host_connection = LocalConnection(play_context=self._play_context, new_stdin='/dev/null')

        self._task.become = False
        self._task.become_flags = None
        self._task.become_method = None
        self._task.become_user = None
        self._task.delegate_to = 'localhost'

        self._play_context.become = False
        self._play_context.become_flags = None
        self._play_context.become_method = None
        self._play_context.become_user = None
        self._play_context.connection = 'local'
        self._play_context.remote_addr = 'localhost'
        self._play_context.remote_user = getpass.getuser()

        self._action_module._connection = host_connection

    def turn_off(self):
        self._task.become = self._cache['t_become']
        self._task.become_flags = self._cache['t_become_flags']
        self._task.become_method = self._cache['t_become_method']
        self._task.become_user = self._cache['t_become_user']
        self._task.delegate_to=self._cache['t_delegate_to']

        self._play_context.become = self._cache['pc_become']
        self._play_context.become_flags = self._cache['pc_become_flags']
        self._play_context.become_method = self._cache['pc_become_method']
        self._play_context.become_user = self._cache['pc_become_user']
        self._play_context.connection = self._cache['pc_connection']
        self._play_context.remote_addr = self._cache['pc_remote_addr']
        self._play_context.remote_user = self._cache['pc_remote_user']

        self._action_module._connection = self._cache['_connection']
