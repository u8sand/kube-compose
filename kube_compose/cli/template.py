from kube_compose.cli import cli
from kube_compose import utils

@cli.command()
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def template(*, helm, name, namespace, docker_compose_config_raw, **_):
  ''' Alias for `helm template [release]`
  '''
  from kube_compose.cli.volume.create import template as volume_create_template
  volume_create_template(volume=None)
  utils.run([
    *helm, 'template',
    *(('-n', namespace) if namespace else tuple()),
    name,
    utils.helm_chart,
    '-f', '-', '--validate=false',
  ], input=docker_compose_config_raw)
