#!/usr/bin/python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import yaml

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase

class Utils:
    @staticmethod
    def concat_vars_dict_to_string(leading_str='', var_dict={}, result=[]):
        for key in var_dict:
            val = var_dict[key]
            result.append(leading_str + key + '=' + val)
        return result

    @staticmethod
    def concat_vars_list_to_string(leading_str='', var_list=[], result=[]):
        for sub_vars in var_list:
            Utils.concat_vars_dict_to_string(leading_str=leading_str,
                                                    var_dict=sub_vars,
                                                    result=result)
        return result

class EnvFileDesc:
    def __init__(self, filename, owner=None, group=None, mode=None, touch=False, comment_symbol='#', export_leading=""):
        self.filename = filename
        self.owner = owner
        self.group = group
        self.mode = mode
        self.touch = touch
        self.comment_symbol = comment_symbol
        self.export_leading = export_leading

    @staticmethod
    def _as_sys_etc_environmenet():
        return EnvFileDesc(filename="/etc/environment", touch=False)

    @staticmethod
    def _as_sys_etc_profile():
        return EnvFileDesc(filename="/etc/profile", touch=False)

    @staticmethod
    def _as_sys_etc_profile_d(filename):
        if filename == None:
            err_msg = (
                "argument 'profile_filename' missing."
            )
            raise AnsibleError(err_msg)
        if not filename.endswith(".sh"):
            err_msg = (
                "Invalid profile_filename '{0}', filename should end with '.sh'".format(filename)
            )
            raise AnsibleError(err_msg)
        return EnvFileDesc(filename=os.path.join("/etc/profile.d/", filename),
                        touch=True,
                        export_leading='export ')

    @staticmethod
    def _as_user_pam_environment(owner_home, owner, group):
        return EnvFileDesc(filename=os.path.join(owner_home, ".pam_environment"),
                        owner=owner,
                        group=group,
                        touch=True)

    @staticmethod
    def _as_user_profile(owner_home, owner, group):
        return EnvFileDesc(filename=os.path.join(owner_home, ".profile"),
                        owner=owner,
                        group=group,
                        touch=True,
                        export_leading="export ")

    @staticmethod
    def _as_user_bashrc(owner_home, owner, group):
        return EnvFileDesc(filename=os.path.join(owner_home, ".bashrc"),
                        owner=owner,
                        group=group,
                        touch=True,
                        export_leading="export ")

    @staticmethod
    def as_sys_env_files(fd, filename):
        if fd == 'etc_env':
            return EnvFileDesc._as_sys_etc_environmenet()
        elif fd == 'etc_profile':
            return EnvFileDesc._as_sys_etc_profile()
        elif fd == 'etc_profd':
            return EnvFileDesc._as_sys_etc_profile_d(filename=filename)
        return None

    @staticmethod
    def as_user_env_files(fd, owner_home, owner, group):
        if fd == 'pam_env':
            return EnvFileDesc._as_user_pam_environment(owner_home=owner_home, owner=owner, group=group)
        elif fd == 'profile':
            return EnvFileDesc._as_user_profile(owner_home=owner_home, owner=owner, group=group)
        elif fd == 'bashrc':
            return EnvFileDesc._as_user_bashrc(owner_home=owner_home, owner=owner, group=group)
        return None


class EnvFileDictDesc:
    def __init__(self):
        dict_file = os.path.join(os.path.dirname(__file__), 'env_edit_dict.yml')
        stream = open(dict_file, "r")
        _dict = {}
        docs = yaml.load_all(stream)
        for doc in docs:
            for key in doc.keys():
                _dict[key] = doc[key]
        self.__dict = _dict

    @staticmethod
    def _merge(a, b):
        if a == None:
            return b
        if b == None:
            return a
        concerns = ['system', 'user']
        # c = {}
        # for k in concerns:
        #     c[k] = b.get(k, a.get(k, None))
        # return c
        c = a.copy()
        c.update(b)
        return c

    @staticmethod
    def _get_next_env_file_vector(dict, def_val, next_path):
        def_key='default'
        next_dict = dict.get(next_path, None)
        if next_dict != None:
            next_dict_default = next_dict.get(def_key, None)
            node_def = EnvFileDictDesc._merge(def_val, next_dict_default)
            return (True, node_def, next_dict)
        return (False, def_val, None)

    @staticmethod
    def _get_env_files(dict, def_val, next_paths =[]):
        if len(next_paths) > 0:
            first = next_paths.pop(0)
            next_lvl = EnvFileDictDesc._get_next_env_file_vector(dict=dict, def_val=def_val, next_path=first)
            if next_lvl[0]:
                return EnvFileDictDesc._get_env_files(dict=next_lvl[2], def_val=next_lvl[1], next_paths=next_paths)
            else:
                return next_lvl[1]
        else:
            return EnvFileDictDesc._merge(def_val, dict)

    def envfiles(self, distribution):
        def_key='default'
        def_node=None

        def_node = self.__dict.get(def_key, def_node)
        path=[distribution.os_family, distribution.name, distribution.release]
        return EnvFileDictDesc._get_env_files(self.__dict, def_val=def_node, next_paths=path)

class Distribution:
    envfile_dict = EnvFileDictDesc()
    def __init__(self, task_vars):
        self.os_family = task_vars.get("ansible_os_family")
        self.name = task_vars.get("ansible_distribution")
        self.release = task_vars.get("ansible_distribution_release")
        self.version = task_vars.get("ansible_distribution_version")
        self.major_version = task_vars.get("ansible_distribution_major_version")

    def user_env_files(self, owner_home='', owner='', group=''):
        efd = Distribution.envfile_dict.envfiles(self)
        env_files=[]
        for f in efd.get('user', []):
            env_files.append(EnvFileDesc.as_user_env_files(f, owner_home=owner_home, owner=owner, group=group))
        return env_files

    def sys_env_files(self, profile_filename):
        efd = Distribution.envfile_dict.envfiles(self)
        env_files=[]
        for f in efd.get('system', []):
            env_files.append(EnvFileDesc.as_sys_env_files(f, filename=profile_filename))
        return env_files

class ActionModule(ActionBase):

    @staticmethod
    def determine_user_env_var_file(task_vars, owner_home='', owner='', group=''):
        user_mode = (len(owner_home) > 0)
        # userhome = task_vars.get('ansible_user_dir', '')
        distribution = Utils.determine_os_distribution(task_vars)
        user_files=[]
        if (distribution['name'] == "Ubuntu"):
            user_files.append(EnvFileDesc.as_user_pam_environment(owner_home=owner_home, owner=owner, group=group))
        return user_files

    @staticmethod
    def determine_sys_env_var_file(task_vars, profile_filename):
        distribution = Utils.determine_os_distribution(task_vars)
        user_files=[]
        if (distribution['name'] == "Ubuntu"):
            user_files.append(EnvFileDesc.as_sys_etc_environmenet())
            # user_files.append(ActionModule.sys_env_var_etc_profile_d(profile_filename))
        return user_files

    def _write_env_var_file(self, task_vars, orig_args, distribution, present=True, env_files=[], tmp=None):
        orig_args_copy = orig_args.copy()
        varlist  = orig_args_copy.get('varlist', None)
        marker = orig_args_copy.get('marker', None)
        comment = orig_args_copy.get('comment', None)
        insertafter = orig_args_copy.get('insertafter', None)
        insertbefore = orig_args_copy.get('insertbefore', None)
        blockinfile_args_tpl = {}
        if insertafter != None:
            blockinfile_args_tpl['insertafter'] = insertafter
        if insertbefore != None:
            blockinfile_args_tpl['insertbefore'] = insertbefore
        step_results =[]
        for ef in env_files:
            if ef == None:
                continue
            blockinfile_args = blockinfile_args_tpl.copy()
            export_leading = ef.export_leading
            comment_symbol = ef.comment_symbol + " "
            lines = []
            if present:
                lines = Utils.concat_vars_list_to_string(leading_str=export_leading,
                                                                var_list=varlist, result=lines)

            blockinfile_args['path'] = ef.filename
            if ef.owner:
                blockinfile_args['owner'] = ef.owner
            if ef.group:
                blockinfile_args['group'] = ef.group
            if ef.mode != None:
                blockinfile_args['mode'] = ef.mode
            if ef.touch:
                blockinfile_args['create'] = 'yes'
            if marker != None:
                fmarker = comment_symbol + marker
                blockinfile_args['marker'] = fmarker
            if comment != None:
                fcomment = comment_symbol + comment
                lines.insert(0, fcomment)
            if present:
                lines_in_string='\n'.join(x for x in lines)
            else:
                lines_in_string=''
            blockinfile_args['block'] = lines_in_string
            step_result = self._execute_module(module_name="blockinfile",
                                          module_args=blockinfile_args,
                                          task_vars=task_vars,
                                          tmp=tmp)
            step_result['EnvFileDesc'] = ef.filename
            failed = step_result.get('failed', False)
            if failed:
                return step_result
            step_results.append(step_result)
        if len(step_results) == 0:
            result={
                'failed': True,
                'changed': False,
                'msg': "Not supported os: [{0} {1} {2} ({3})]"
                    .format(distribution.os_family, distribution.name, distribution.version, distribution.release)
            }
            return result
        else:
            result = {}
            files_string=', '.join(x.get('EnvFileDesc') for x in step_results)
            if len(step_results) == 1:
                result = step_results[0]
            else:
                result={
                    'changed': False,
                    'step_results': step_results
                }
                for sr in step_results:
                    if sr.get('changed', False):
                        result['changed'] = True
            result['msg'] = "Update Enviroment Variables -> " + files_string
            # result['_ansible_verbose_always'] = True
            return result


    def run(self, tmp=None, task_vars=None):
        orig_args = self._task.args
        if task_vars is None:
            task_vars = dict()

        owner = orig_args.get('owner', None)
        group = orig_args.get('group', None)
        owner_home = None
        if owner:
            owner_home = '~' + owner

        profile_filename = orig_args.get('profile_filename', None)

        user_mode = bool(owner_home)
        distribution = Distribution(task_vars=task_vars)
        if user_mode:
            env_files = distribution.user_env_files(owner_home=owner_home,
                                                    owner=owner,
                                                    group=group)
        else:
            env_files = distribution.sys_env_files(profile_filename=profile_filename)
        present = (orig_args.get('state', 'present') == 'present')
        result = self._write_env_var_file(task_vars=task_vars, orig_args=orig_args, present=present,
                                 env_files=env_files, tmp=tmp, distribution=distribution)

        return result
