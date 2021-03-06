import logging
import os
from time import sleep

import keystoneauth1.loading
import keystoneauth1.session
import heatclient.client
import novaclient.client
from heatclient.common import template_utils

logger = logging.getLogger(__name__)


class CPUStressResource(object):
    def __init__(self, context):
        resource = context.v1.resource
        self.heat_stack_name = resource.name
        keystone_password_loader = keystoneauth1.loading.get_plugin_loader(
            'password')
        auth = keystone_password_loader.load_from_options(
            auth_url=resource.params['auth_url'],
            username=resource.params['username'],
            password=resource.params['password'],
            project_name=resource.params['project_name'])
        keystone_session = keystoneauth1.session.Session(auth=auth)
        self._heat = heatclient.client.Client('1', session=keystone_session)
        self._nova = novaclient.client.Client('2', session=keystone_session)
        self.endpoint = {}
        self.template_path = self.get_template_path()

    def get_template_path(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        template_path = os.path.join(
            script_dir, '../templates/cpu-stress-stack.yaml')
        template_path = os.path.normpath(template_path)
        return template_path

    def deploy(self, context):
        heat_stack_args = self._create_heat_stack_args()
        self._heat.stacks.create(**heat_stack_args)
        self._wait_for_stack_complete()
        self.endpoint = {'url': 'url', 'user': 'user', 'password': 'password'}

    def _create_heat_stack_args(self):
        tpl_files, template = template_utils.get_template_contents(
            self.template_path)
        args = {
            'stack_name': self.heat_stack_name,
            'template': template,
            'files': tpl_files,
            'parameters': {
                'public_net_id': 'public',
                'private_net_id': 'private-1a03e53738ad4854b9610273945c2b6b',
                'private_subnet_id': '30e4947e-6479-419c-8f85-a20c993bb939',
            },
        }
        return args

    def _wait_for_stack_complete(self):
        while True:
            sleep(5)
            stack = self._heat.stacks.get(self.heat_stack_name)
            status = stack.stack_status
            if status == 'CREATE_COMPLETE':
                return
            if status == 'CREATE_FAILED':
                raise Exception('Stack create failed')

    def clean(self, context):
        logger.warning('Skip clean resources for cpu-stress-stack')
        self._heat.stacks.delete(self.heat_stack_name)
        self._wait_for_stack_deleted()

    def _wait_for_stack_deleted(self):
        while True:
            sleep(5)
            try:
                stack = self._heat.stacks.get(self.heat_stack_name)
                status = stack.stack_status
            except Exception:
                status = False
            if status == 'DELETE_COMPLETE' or not status:
                return
            if status == 'DELETE_FAILED':
                raise Exception('Stack delete failed')
