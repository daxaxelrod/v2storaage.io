# from storaage import *

from peewee_migrate.core import Router


router = Router('migrations', DATABASE='storage')
# create migration

router.create('migration_v2')

router.run('migration_v2')

router.run()
