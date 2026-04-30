#!/usr/bin/env python3
"""
Zenthral CLI - Main entry point
"""
import click
import sys
from .commands import auth, config, run, daemon, workflows, logs

@click.group()
@click.version_option(version='0.1.0')
def main():
    """Zenthral CLI - Execute AI automation workflows locally"""
    pass

# Register command groups
main.add_command(auth.login)
main.add_command(auth.logout)
main.add_command(auth.whoami)
main.add_command(config.config)
main.add_command(run.run)
main.add_command(daemon.daemon)
main.add_command(workflows.list_workflows)
main.add_command(workflows.test)
main.add_command(workflows.validate)
main.add_command(logs.logs)
main.add_command(workflows.status)

if __name__ == '__main__':
    main()
