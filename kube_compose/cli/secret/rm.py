import click
from kube_compose import utils
from kube_compose.cli.secret import secret

@secret.command('rm')
@click.argument('secret', type=str, required=False)
def _(**kwargs):
  ''' Remove a kubernetes secret
  '''
  rm(**kwargs)

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def rm(*, secret, docker_compose_config, context, namespace, kubectl, **_):
  for secret in ([secret] if secret is not None else [
    secret for secret, secret_config in docker_compose_config.get('secrets', {}).items()
    if not secret_config.get('external')
  ]):
    utils.run([
      *kubectl,
      *(['--context', context] if context else []),
      *(['-n', namespace] if namespace else []),
      'delete',
      f"secret/{secret}",
    ])
