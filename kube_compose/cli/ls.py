import json
from kube_compose.cli import cli
from kube_compose import utils

@cli.command()
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def ls(*, namespace, helm, **_):
  ''' Like `docker-compose ls` but shows the docker-compose releases
  '''
  utils.echo_table_via_pager(
    [('NAME', 'NAMESPACE', 'REVISION', 'UPDATED', 'STATUS')] + [
    (release['name'], release['namespace'], release['revision'], release['updated'], release['status'])
    for release in json.loads(
      utils.check_output([
        helm, 'list',
        *(('-n', namespace) if namespace else ('-A',)),
        '-o', 'json',
      ])
    )
    if release['chart'].startswith('kube-compose-')
  ])
