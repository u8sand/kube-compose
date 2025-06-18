from kube_compose.cli import cli
from kube_compose import utils

@cli.group()
def get():
  ''' Access helm chart values
  '''
  pass

@get.command('all')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def get_all(*, name, namespace, helm, **_):
  ''' download all information for a named release
  '''
  utils.run([*helm, 'get', 'all', *(('-n', namespace) if namespace else tuple()), name])

@get.command('manifest')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def get_manifest(*, name, namespace, helm, **_):
  ''' download the manifest for a named release
  '''
  utils.run([*helm, 'get', 'manifest', *(('-n', namespace) if namespace else tuple()), name])

@get.command('metadata')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def get_metadata(*, name, namespace, helm, **_):
  ''' This command fetches metadata for a given release
  '''
  utils.run([*helm, 'get', 'metadata', *(('-n', namespace) if namespace else tuple()), name])

@get.command('values')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def get_values(*, name, namespace, helm, **_):
  ''' download the values file for a named release
  '''
  utils.run([*helm, 'get', 'values', *(('-n', namespace) if namespace else tuple()), name])
