"""
Controller for /admin service. Includes fixtures (seed data).

Defines all required seed data to be populated into database on first run.
Includes test user accounts, global variables, business logic requirements,
administrative settings, and ID/description pairs for lookup tables.

More info: http://thadeusb.com/weblog/2010/4/21/using_fixtures_in_web2py

Author: Henry Nguyen (henry@dxconcept.com)
"""


def reset_database():
    logger.info("Doing a full reset of the database...")
    db.executesql('SET FOREIGN_KEY_CHECKS=0;')
    truncate_tables()
    plant_seed_data()
    populate_test_data()
    db.executesql('SET FOREIGN_KEY_CHECKS=1;')


def truncate_tables():
    # truncate ALL database tables.
    table_truncate_order = [
        'contact',
        'user_settings',
        'system_settings',
        'auth_cas',
        'auth_event',
        'auth_group',
        'auth_membership',
        'auth_permission',
        'auth_user',
    ]

    for table in table_truncate_order:
        logger.info("Truncating", table)
        db[table].truncate()

    logger.info("Completed truncate_tables()")


def plant_seed_data():
    # Nothing to plant... yet...
    logger.info("Completed plant_seed_data()")


def populate_test_data():
    admin_group = auth.add_group('admin', 'admin')
    admin_user = db.auth_user.validate_and_insert(username='admin', password='asdfasdf')
    auth.add_membership(admin_group, admin_user)

    test_user = db.auth_user.validate_and_insert(username='test', password='asdfasdf')

    logger.info("Completed populate_test_data()")
