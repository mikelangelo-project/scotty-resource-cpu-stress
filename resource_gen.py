import logging

from cpustress.resource import CPUStressResource

logger = logging.getLogger(__name__)

cpu_stress_resource = None


def deploy(context):
    logger.info('Deploy iperf with heat')
    global cpu_stress_resource
    cpu_stress_resource = CPUStressResource(context)
    cpu_stress_resource.deploy(context)
    return cpu_stress_resource.endpoint


def clean(context):
    cpu_stress_resource.clean(context)
