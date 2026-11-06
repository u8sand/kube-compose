from kube_compose.cli import cli

@cli.group()
def secret():
  ''' Manipulate kubernetes secrets like docker secrets
  '''
  pass
