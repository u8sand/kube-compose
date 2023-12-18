import click
from kube_compose.cli import cli
from kube_compose import utils

@cli.command()
@click.option('-v', '--volumes', type=bool, is_flag=True, help='Remove named volumes declared in the "volumes" section')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def down(*, helm, name, namespace, volumes, **_):
  ''' Like `docker-compose down` but stops the kubernetes deployed resources
  '''
  utils.run([
    helm, 'uninstall',
    *(('-n', namespace) if namespace else tuple()),
    name,
  ])
  if volumes:
    from kube_compose.cli.volume.rm import rm
    rm(volume=None)
