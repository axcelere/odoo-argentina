from odoo import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute("""
        DELETE FROM account_account_tag_account_tax_repartition_line_rel
        WHERE account_account_tag_id = 24
    """)
    _logger.info('L10n Latam Check Adhoc Executing pre init method')
    cr.execute('''
        ALTER TABLE account_payment_method
        DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique;
    ''')
    for rec in env['account.payment.method'].search([]):
        rec.write({'code': '%s-%s' % (rec.code, 'old')})
