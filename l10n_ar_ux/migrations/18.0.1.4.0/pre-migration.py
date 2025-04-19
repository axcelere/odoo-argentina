from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """
    The objective of this is delete the original view form the module how bring the functionality
    adding in the previous commit
    """
    cr.execute("""
        DELETE FROM account_account_tag_account_tax_repartition_line_rel
        WHERE account_account_tag_id = 24
    """)
