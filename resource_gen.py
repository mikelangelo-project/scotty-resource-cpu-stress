import logging

from cpustress.resource import CPUStressResource

logger = logging.getLogger(__name__)

cpu_stress_resource = None


def deploy(context):
    reduce_logging()
    logger.info('Deploy cpu-stress with heat')
    global cpu_stress_resource
    cpu_stress_resource = CPUStressResource(context)
    cpu_stress_resource.deploy(context)
    return cpu_stress_resource.endpoint


def clean(context):
    cpu_stress_resource.clean(context)


def reduce_logging():
    reduce_loggers = {
        'keystoneauth.identity.v2', 'keystoneauth.identity.v2.base',
        'keystoneauth.session', 'urllib3.connectionpool', 'stevedore.extension'
    }
    for logger in reduce_loggers:
        logging.getLogger(logger).setLevel(logging.WARNING)
