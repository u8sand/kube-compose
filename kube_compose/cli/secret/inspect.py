import click
from kube_compose import utils
from kube_compose.cli.secret import secret

@secret.command('inspect')
@click.argument('secret', type=str, required=True)
def _(**kwargs):
  ''' Inspect a kubernetes secret
  '''
  inspect(**kwargs)

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def inspect(*, secret, context, namespace, kubectl, **_):
  utils.run([
    *kubectl,
    *(['--context', context] if context else []),
    *(['-n', namespace] if namespace else []),
    'get',
    f"secret/{secret}",
    '-o', 'yaml',
  ])
