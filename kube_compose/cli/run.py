import json
import time
import uuid
import click
from kube_compose import utils
from kube_compose.cli import cli

def _wait_for_container_state(kubectl_base, name, *, terminated=False, timeout=60):
  deadline = time.monotonic() + timeout
  while time.monotonic() < deadline:
    status = json.loads(utils.check_output([
      *kubectl_base, 'get', 'pod', name, '-o', 'json',
    ])).get('status', {})
    container_statuses = status.get('containerStatuses', [])
    state = container_statuses[0].get('state', {}) if container_statuses else {}
    if 'terminated' in state or (not terminated and 'running' in state):
      return state
    time.sleep(0.1)
  raise click.ClickException(f'timed out waiting for pod/{name} container state')

@cli.command(context_settings={"ignore_unknown_options": True})
@utils.require_binaries(kubectl='kubectl')
@utils.require_kube_compose_release
@click.option('-i', '--stdin', type=bool, is_flag=True)
@click.option('-t', '--tty', type=bool, is_flag=True)
@click.argument('service', type=str)
@click.argument('args', nargs=-1, type=str)
def run(*, service, args, stdin, tty, context, namespace, docker_compose_config, kubectl, **_):
  ''' Like `docker-compose run` but for the kubernetes deployed resources
  '''
  service_config = docker_compose_config['services'][service]
  name = f"{service}-{uuid.uuid4()}"
  overrides = {
    'spec': {
      'containers': [{
        'name': name,
        'image': service_config['image'],
        'tty': tty,
        'stdin': stdin,
      }],
    },
  }
  #
  if args:
    # args come from the shell (not compose), so they need escaping for kubernetes' `$(VAR)` expansion
    c, *a = map(utils.k8s_escape, args)
    overrides['spec']['containers'][0]['command'] = [c]
    overrides['spec']['containers'][0]['args'] = [*a]
  #
  if service_config.get('environment'):
    overrides['spec']['containers'][0]['env'] = [
      {
        'name': key,
        'value': value,
      }
      for key, value in service_config.get('environment', {}).items()
    ]
  #
  if service_config.get('volumes'):
    overrides['spec']['containers'][0]['volumeMounts'] = []
    overrides['spec']['volumes'] = []
    for volume in service_config['volumes']:
      from kube_compose.cli.volume.create import create
      create(volume=volume['source'])
      overrides['spec']['containers'][0]['volumeMounts'].append(
        {
          'mountPath': volume['target'],
          'name': volume['source'],
        }
      )
      overrides['spec']['volumes'].append(
        {
          'name': volume['source'],
          'persistentVolumeClaim': {
            'claimName': volume['source'],
          },
        }
      )
  #
  kubectl_base = [
    *kubectl,
      *(['--context', context] if context else []),
      *(['-n', namespace] if namespace else []),
  ]
  utils.run([
      *kubectl_base,
      'run',
      name,
      '--restart=Never',
      f"--image={service_config['image']}",
      '--overrides', json.dumps(overrides),
      *(('--command', '--', *map(utils.k8s_escape, args)) if args else tuple()),
  ])
  try:
    state = _wait_for_container_state(kubectl_base, name)
    if stdin or tty:
      if 'terminated' in state:
        utils.run([*kubectl_base, 'logs', name], check=False)
      else:
        attach_returncode = utils.run([
          *kubectl_base, 'attach', name,
          *(('-i',) if stdin else tuple()),
          *(('-t',) if tty else tuple()),
        ], check=False)
        # The container can finish between observing it running and attaching to it.
        if attach_returncode:
          utils.run([*kubectl_base, 'logs', name], check=False)
    else:
      utils.run([
        *kubectl_base, 'logs',
        *(('-f',) if 'running' in state else tuple()),
        name,
      ])

    state = _wait_for_container_state(kubectl_base, name, terminated=True)
    if state['terminated'].get('exitCode'):
      raise click.exceptions.Exit(state['terminated']['exitCode'])
  finally:
    utils.run([
      *kubectl_base, 'delete', 'pod', name,
      '--ignore-not-found=true',
      '--wait=false',
    ], check=False)
