import click
from kube_compose import utils

@click.group()
@click.version_option()
@click.option('-f', '--file', help='Compose configuration files')
@click.option('--profile', 'profiles', multiple=True,
  callback=lambda ctx, param, values: tuple(p for value in values for p in value.split(',') if p),
  help='Enable a compose profile (may be repeated or comma-separated)')
@utils.set_group_config
def cli(**kwargs): pass
