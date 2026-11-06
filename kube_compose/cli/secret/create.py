import os
import base64
import yaml
import click
from kube_compose import utils
from kube_compose.cli.secret import secret

def create_secret_spec(*, secret, docker_compose_path, docker_compose_config, **_):
  secret_specs = []
  for secret, secret_config in ([(secret, docker_compose_config['secrets'][secret],)] if secret is not None else docker_compose_config.get('secrets', {}).items()):
    if secret_config.get('external'): continue
    secret_ext_config = utils.compose_unescape(secret_config.get('x-kubernetes', {}))
    secret_spec = {
      'apiVersion': 'v1',
      'kind': 'Secret',
      'metadata': {
        'name': secret,
        'labels': dict({'app.kubernetes.io/managed-by': 'kube-compose'}, **secret_ext_config.get('labels', {})),
        'annotations': secret_ext_config.get('annotations', {}),
      },
      'type': 'Opaque',
      'data': {}
    }
    if 'file' in secret_config:
      content = (docker_compose_path.parent / secret_config['file']).read_bytes()
    elif 'environment' in secret_config:
      content = os.environ[secret_config['environment']].encode()
    else:
      raise NotImplementedError('secret could not be located')
    secret_spec['data']['content'] = base64.b64encode(content).decode()
    secret_specs.append(secret_spec)
  return secret_specs

@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
def create(*, secret, docker_compose_path, docker_compose_config, context, namespace, kubectl, **_):
  secret_specs = create_secret_spec(
    secret=secret,
    docker_compose_path=docker_compose_path,
    docker_compose_config=docker_compose_config,
    kubectl=kubectl,
  )
  if not secret_specs: return
  utils.run([
    *kubectl,
    *(['--context', context] if context else []),
    *(['-n', namespace] if namespace else []),
    'apply',
    '-f', '-',
  ], input=yaml.dump_all(secret_specs).encode())

@secret.command('create')
@click.argument('secret', type=str, required=False)
def _(**kwargs):
  ''' Ensure a kubernetes secret is created
  '''
  create(**kwargs)
