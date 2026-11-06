from kube_compose import utils
from kube_compose.cli.secret import secret

@secret.command('ls')
def _(**kwargs):
  ''' List kubernetes secrets
  '''
  ls(**kwargs)

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def ls(*, context, namespace, kubectl, **_):
  utils.run([
    *kubectl,
    *(['--context', context] if context else []),
    *(['-n', namespace] if namespace else []),
    'get',
    'secret',
  ])
