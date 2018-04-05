# -*- coding: utf-8 -*-

import os
import pytest
import subprocess

from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from os import path

MIGRATION_PATH = path.join(path.dirname(__file__), '..', 'alembic', 'versions')

ALL_MIGRATIONS = [x.split('.')[0].split('_')[0]
                  for x in os.listdir(MIGRATION_PATH)
                  if x.endswith('.py')]


def list_migrations(cfg_path, head):
    cfg = AlembicConfig(cfg_path)
    script = ScriptDirectory.from_config(cfg)
    migrations = [x.revision
                  for x in script.walk_revisions(base='base', head=head)]
    migrations.reverse()
    return migrations


def upgrade(alembic_config, migration):
    subprocess.check_call(['alembic', 'upgrade', migration],
                          cwd=path.dirname(alembic_config))


def downgrade(alembic_config, migration):
    subprocess.check_call(['alembic', 'downgrade', migration],
                          cwd=path.dirname(alembic_config))


@pytest.mark.parametrize('migration', ALL_MIGRATIONS)
def test_alembic_migration_upgrade(alembic_config, config, migration):
    # run migrations in sequence from base -> head
    for mig in list_migrations(alembic_config, migration):
        upgrade(alembic_config, mig)


@pytest.mark.parametrize('migration', ALL_MIGRATIONS)
def test_alembic_migration_downgrade(alembic_config, config, migration):
    # upgrade to the parameterized test case ("head")
    upgrade(alembic_config, migration)

    # run migrations in sequence from "head" -> base
    migrations = list_migrations(alembic_config, migration)
    migrations.reverse()

    for mig in migrations:
        downgrade(alembic_config, mig)