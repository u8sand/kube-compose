import sys
import yaml
import click
from kube_compose import utils
from kube_compose.cli.secret import secret
from kube_compose.cli.secret.create import create_secret_spec

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def template(*, secret, docker_compose_path, docker_compose_config, context, namespace, kubectl, **_):
  secret_specs = create_secret_spec(
    secret=secret,
    docker_compose_path=docker_compose_path,
    docker_compose_config=docker_compose_config,
    kubectl=kubectl,
  )
  if not secret_specs: return []
  # use kubectl to fill-in defaults/validate
  templ = yaml.safe_load(utils.check_output([
    *kubectl,
    *(['--context', context] if context else []),
    *(['-n', namespace] if namespace else []),
     'apply',
    '--dry-run=client',
    '-oyaml',
    '-f', '-',
  ], input=yaml.dump_all(create_secret_spec(
    secret=secret,
    docker_compose_path=docker_compose_path,
    docker_compose_config=docker_compose_config,
    kubectl=kubectl,
  )).encode()))
  # write items in flat yaml format
  if templ['kind'] == 'List':
    return templ['items']
  else:
    return [templ]

@secret.command('template')
@click.argument('secret', type=str, required=False)
def _(**kwargs):
  ''' Template a kubernetes secret
  '''
  yaml.dump_all(template(**kwargs), sys.stdout)
