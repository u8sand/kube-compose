import json
import click
from kube_compose import utils
from kube_compose.cli.volume import volume

@volume.command('create')
@click.argument('volume', type=str, required=False)
def _(**kwargs):
  ''' Ensure a kubernetes persistent volume is created
  '''
  create(**kwargs)

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def create(*, volume, docker_compose_config, namespace, kubectl, **_):
  for volume, volume_config in ([(volume, docker_compose_config['volumes'][volume],)] if volume is not None else docker_compose_config.get('volumes', {}).items()):
    volume_ext_config = volume_config.get('x-kubernetes', {})
    utils.run([
      kubectl, 'apply',
      *(('-n', namespace) if namespace else tuple()),
      '-f', '-',
    ], input=json.dumps({
      'apiVersion': 'v1',
      'kind': 'PersistentVolumeClaim',
      'metadata': {
        'name': volume,
        'namespace': namespace or 'default',
      },
      'spec': {
        'accessModes': [volume_ext_config.get('mode', 'ReadWriteOnce')],
        'resources': {
          'requests': {
            'storage': volume_ext_config.get('size', '1Gi'),
          },
        },
        'storageClassName': volume_ext_config.get('class', ''),
        'volumeMode': 'Filesystem',
      },
    }).encode())
