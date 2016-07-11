import click

from nsone.config import ConfigException
from ns1cli.cli import cli
from ns1cli.util import Formatter


class ConfigFormatter(Formatter):

    def print_config(self, config):
        try:
            click.secho('Current Key: %s' % config.getCurrentKeyID(), bold=True)
            self.pretty_print(config.getKeyConfig())
        except ConfigException as e:
            pass

        self.out(config)


@click.group('config',
             short_help='view and modify local configuration settings')
@click.pass_context
def cli(ctx):
    """View and manipulate configuration settings"""
    ctx.obj.formatter = ConfigFormatter(ctx.obj.get_config('output_format'))


@cli.command('show', short_help='show the existing config')
@click.pass_context
def show(ctx):
    """Show the existing config

    \b
    EXAMPLES:
        ns1 config show
    """
    ctx.obj.formatter.print_config(ctx.obj.rest.config)


@cli.command('set', short_help='set the configuration key-value')
@click.argument('KEY')
@click.argument('VALUE')
@click.pass_context
def set(ctx, value, key):
    """Set the active configuration key-value

    \b
    EXAMPLES:
        ns1 config set write_lock true
        ns1 config set output_format json
    """
    ctx.obj.set_config(key, value)
    ctx.obj.formatter.print_config(ctx.obj.rest.config)


@cli.command('key', short_help='set the active configuration key ID')
@click.argument('KEYID')
@click.pass_context
def key(ctx, keyid):
    """Set the active configuration key ID

    \b
    EXAMPLES:
        ns1 config key default
    """
    try:
        ctx.obj.rest.config.useKeyID(keyid)
        click.secho('Using Key: %s' % keyid, bold=True)
        click.secho('Endpoint: %s' % ctx.obj.rest.config.getEndpoint(), bold=True)
    except ConfigException as e:
        raise click.ClickException(e.message)
