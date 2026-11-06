import sys
import yaml
import click
from kube_compose import utils
from kube_compose.cli.volume import volume
from kube_compose.cli.volume.create import create_volume_spec

@utils.require_kube_compose_release
def template(*, volume, docker_compose_config, **_):
  # NOTE: this is purely client side (like `helm template`), the specs are emitted as-is
  return create_volume_spec(
    volume=volume,
    docker_compose_config=docker_compose_config,
  )

@volume.command('template')
@click.argument('volume', type=str, required=False)
def _(**kwargs):
  ''' Ensure a kubernetes persistent volume is templated
  '''
  yaml.dump_all(template(**kwargs), sys.stdout)
