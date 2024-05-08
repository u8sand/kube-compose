import click
import pathlib
import functools

__dir__ = pathlib.Path(__file__).parent

helm_chart = str(__dir__ / 'charts' / 'kube-compose')

def assert_defined(value, or_else):
  assert value, or_else
  return value

def pathlib_coalesce(*paths):
  for path in map(pathlib.Path, paths):
    if path.exists(): return path
  if not paths: raise RuntimeError('No paths to check')
  else: raise FileNotFoundError(paths[0])

@click.pass_context
def run(ctx: click.Context, *args, input=None, **kwargs):
  ''' Similar to subprocess.run but
  1. forward Ctrl+C
  2. exit click application with exitcode of the process
  '''
  import signal
  import subprocess
  if input: kwargs['stdin'] = subprocess.PIPE
  p = subprocess.Popen(*args, **kwargs)
  if input:
    p.stdin.write(input)
    p.stdin.close()
  while p.returncode is None:
    try:
      p.wait()
    except KeyboardInterrupt:
      p.send_signal(signal.SIGINT)
    except:
      p.kill()
      p.wait()
      raise
  if p.returncode != 0:
    ctx.exit(p.returncode)

@click.pass_context
def check_output(ctx: click.Context, *args, **kwargs):
  ''' Similar to subprocess.check_output but exit click application with exitcode of the process on error
  '''
  import subprocess
  try:
    return subprocess.check_output(*args, **kwargs)
  except subprocess.CalledProcessError as e:
    ctx.exit(e.returncode)

def require_binaries(**required_binaries):
  ''' Ensure binaries are present, and inject the paths to them in kwargs
  Usage:
  @require_binaries(curl_bin='curl')
  def whats_my_ip(*, curl_bin):
    return check_output([curl_bin, '-s', 'https://ifconfig.me']).decode()
  '''
  def decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
      from shutil import which
      binaries = {
        arg: assert_defined(which(binary), f"{binary} command not found")
        for arg, binary in required_binaries.items()
      }
      return fn(*args, **dict(binaries, **kwargs))
    return wrapper
  return decorator

def echo_table_via_pager(records):
  import click
  colSize = {}
  for record in records:
    for i, cell in enumerate(record):
      colSize[i] = max(colSize[i], len(cell)) if i in colSize else len(cell)
  click.echo_via_pager([
    ' '.join(('{:^%d}' % (colSize[i])).format(cell) for i, cell in enumerate(record)) + '\n'
    for record in records
  ])

def require_kube_compose_release(fn):
  @functools.wraps(fn)
  @require_binaries(docker='docker')
  def wrapper(*, docker, **kwargs):
    import yaml
    docker_compose_config_raw = check_output([docker, 'compose', 'config'])
    docker_compose_config = yaml.safe_load(docker_compose_config_raw)
    if 'x-kubernetes' not in docker_compose_config:
      raise click.ClickException('top-level `x-kubernetes` map with release `name` and `namespace` is required')
    release_config = docker_compose_config['x-kubernetes']
    name = release_config['name']
    namespace = release_config.get('namespace')
    return fn(**dict(kwargs,
      docker=docker,
      docker_compose_config_raw=docker_compose_config_raw,
      docker_compose_config=docker_compose_config,
      release_config=release_config,
      name=name,
      namespace=namespace,
    ))
  return wrapper
