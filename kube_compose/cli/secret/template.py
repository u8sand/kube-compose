import sys
import yaml
import click
from kube_compose import utils
from kube_compose.cli.secret import secret
from kube_compose.cli.secret.create import create_secret_spec

@utils.require_kube_compose_release
def template(*, secret, docker_compose_path, docker_compose_config, **_):
  # NOTE: this is purely client side (like `helm template`), the specs are emitted as-is
  return create_secret_spec(
    secret=secret,
    docker_compose_path=docker_compose_path,
    docker_compose_config=docker_compose_config,
  )

@secret.command('template')
@click.argument('secret', type=str, required=False)
def _(**kwargs):
  ''' Template a kubernetes secret
  '''
  yaml.dump_all(template(**kwargs), sys.stdout)
