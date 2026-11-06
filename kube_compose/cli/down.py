import click
from kube_compose.cli import cli
from kube_compose import utils

@cli.command()
@click.option('-v', '--volumes', type=bool, is_flag=True, help='Remove named volumes/configmaps/secrets declared in the "volumes"/"configs"/"secrets" sections')
@utils.require_binaries(helm='helm')
@utils.require_kube_compose_release
def down(*, helm, name, context, namespace, volumes, **_):
  ''' Like `docker-compose down` but stops the kubernetes deployed resources
  '''
  utils.run([
    *helm,
    *(['--kube-context', context] if context else []),
    *(['-n', namespace] if namespace else []),
    'uninstall',
    name,
  ])
  if volumes:
    from kube_compose.cli.volume.rm import rm as volume_rm
    from kube_compose.cli.configmap.rm import rm as configmap_rm
    from kube_compose.cli.secret.rm import rm as secret_rm
    volume_rm(volume=None)
    configmap_rm(configmap=None)
    secret_rm(secret=None)
