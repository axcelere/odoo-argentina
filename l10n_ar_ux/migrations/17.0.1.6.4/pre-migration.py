from openupgradelib import openupgrade
import logging

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'l10n_ar_ux.report_invoice_document',
            'l10n_ar_ux.view_account_invoice_line_report_tree',
            'l10n_ar_edi.report_invoice_document',
            'l10n_ar_edi_ux.view_account_journal_tree',
            'l10n_ar_edi_ux.view_account_payment_form_inherited',
        ],
        delete_childs=True
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'l10n_ar_ux.report_payment_group_document',
        ],
        delete_childs=True
    )
