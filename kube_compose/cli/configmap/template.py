import sys
import yaml
import click
from kube_compose import utils
from kube_compose.cli.configmap import configmap
from kube_compose.cli.configmap.create import create_configmap_spec

@utils.require_kube_compose_release
def template(*, configmap, docker_compose_path, docker_compose_config, **_):
  # NOTE: this is purely client side (like `helm template`), the specs are emitted as-is
  return create_configmap_spec(
    configmap=configmap,
    docker_compose_path=docker_compose_path,
    docker_compose_config=docker_compose_config,
  )

@configmap.command('template')
@click.argument('configmap', type=str, required=False)
def _(**kwargs):
  ''' Template a kubernetes configmap
  '''
  yaml.dump_all(template(**kwargs), sys.stdout)
