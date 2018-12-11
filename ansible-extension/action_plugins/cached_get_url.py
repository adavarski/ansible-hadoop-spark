#!/usr/bin/python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os, imp
import errno
import fcntl

_localcall_path = os.path.join(os.path.dirname(__file__), "_localcall.py")
localcall = imp.load_source('', _localcall_path)

from ansible.inventory.host import Host
from ansible.module_utils._text import to_text
from ansible.plugins.action.copy import ActionModule as CopyActionModule

class ActionModule(CopyActionModule):
    _get_url_compatible_args = [
        "url",
        "force",
        "http_agent",
        "use_proxy",
        "validate_certs",
        "url_username",
        "url_password",
        "force_basic_auth",
        "client_cert",
        "client_key",
        "dest",
        "backup",
        "sha256sum",
        "checksum",
        "timeout",
        "headers",
        "tmp_dest",
    ]
    _get_url_incompatible_args = [
        "original_basename",
        "content",
        "cached",
    ]
    _copy_compatible_args = [
        "src",
        "original_basename",
        "content",
        "dest",
        "backup",
        "force",
        "validate",
        "directory_mode",
        "remote_src",
        "local_follow"
    ]
    _copy_incompatible_args = [
        "url",
        "cached",
        "validate_certs",
        "http_agent",
        "use_proxy",
        "validate_certs",
        "url_username",
        "url_password",
        "force_basic_auth",
        "client_cert",
        "client_key",
        "backup",
        "sha256sum",
        "checksum",
        "timeout",
        "headers",
        "tmp_dest",
    ]

    @staticmethod
    def _keep_compatible (_dict, compatible_keys):
        to_del_keys = []
        for k in _dict.keys():
            if k not in compatible_keys:
                to_del_keys.append(k)
        for k in to_del_keys:
            _dict.pop(k)

    @staticmethod
    def _drop_incompatible (_dict, incompatible_keys):
        to_del_keys = []
        for k in _dict.keys():
            if k in incompatible_keys:
                to_del_keys.append(k)
        for k in to_del_keys:
            _dict.pop(k)


    def _local_get_url (self, task_vars, task_args):
        task = self._task
        loader = self._loader
        variable_manager = self._task._variable_manager
        inventory = variable_manager._inventory
        host = inventory.get_host(task_vars['inventory_hostname'])
        play_context = self._play_context

        cached  = task_args.get('cached', None)
        play = task._role._play

        # Update task_args
        new_task_args = task_args.copy()
        new_task_args.pop('cached')
        new_task_args['dest'] = cached

        # Save call-context
        local_switch = localcall.Switch2Local(task=task, play_context=play_context, action_module=self)
        try:
            # Set call-context
            local_switch.turn_on()

            localhost = Host('localhost')
            new_task_vars = variable_manager.get_vars(play=play, host=localhost, task=self._task)
            module_ret = self._execute_module(module_name="get_url",
                                              module_args=new_task_args,
                                              task_vars=new_task_vars,
                                              tmp=None)
        finally:
            # Un-Set call-context
            local_switch.turn_off()
        return module_ret

    def run(self, tmp=None, task_vars=None):
        orig_args = self._task.args
        orig_args_copy = orig_args.copy()
        if task_vars is None:
            task_vars = dict()

        cached  = orig_args_copy.get('cached', None)
        # cached = to_bytes(cached, errors='surrogate_or_strict')
        cache_exist = os.path.exists(cached)
        cached_dir = os.path.dirname(cached)
        if not os.path.exists(cached_dir):
            try:
                os.makedirs(cached_dir, 0777)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(cached_dir):
                    pass
                else:
                    raise

        call_path = []
        cached_file_lock = cached + ".lock"
        local_get_res = None
        if not cache_exist:
            lock_file = open(cached_file_lock, "w")
            lock_file.write(orig_args_copy['url'])
            lock_file.close()
            local_get_suc = False
            try:
                lock_file = open(cached_file_lock, "r")
                lock_fd = lock_file.fileno()

                fcntl.flock(lock_fd, fcntl.LOCK_EX)
                cache_exist = os.path.exists(cached)
                if not cache_exist :
                    local_get_res = self._local_get_url(task_vars, orig_args_copy)
                    local_get_suc = not local_get_res.get('failed', False);
                    if local_get_suc:
                        call_path.append('local.get_url.ok')
                    else:
                        call_path.append('local.get_url.failed:%s' % (local_get_res.get('msg', '')))
            finally:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_file.close()

            if local_get_suc:
                try:
                    os.remove(cached_file_lock)
                except Exception as e:
                    call_path.append(u"delete lock file exception: %s" % to_text(e))

        cache_exist = os.path.exists(cached)
        if cache_exist:
            local_task_args = orig_args.copy()
            local_task_args['src'] = cached
            ActionModule._drop_incompatible(local_task_args, ActionModule._copy_incompatible_args)
            self._task.args = local_task_args
            result = super(ActionModule, self).run(tmp, task_vars)
            self._task.args = orig_args
            call_path.append('copy')
            if os.path.exists(cached_file_lock):
                try:
                    os.remove(cached_file_lock)
                except Exception as e:
                    call_path.append(u"delete lock file exception: %s" % to_text(e))
        else:
            local_task_args = orig_args.copy()
            ActionModule._drop_incompatible(local_task_args, ActionModule._get_url_incompatible_args)
            result = self._execute_module(module_name="get_url",
                                              module_args=local_task_args,
                                              task_vars=task_vars,
                                              tmp=tmp)
            call_path.append('remote.get_url')

        final_suc = not result.get('failed', False);
        path_msg = ", ".join(call_path)
        path_msg = result.get('msg', '') + "(Call-path: " + path_msg + ")"
        result['msg'] = path_msg
        result['local_get_url'] = local_get_res
        if not final_suc:
            result['_ansible_verbose_always'] = True
        return result
