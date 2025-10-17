from openupgradelib import openupgrade
import logging

logger = logging.getLogger(__name__)

@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'l10n_ar_withholding_ux.res_config_settings_view_form',
        ],
        delete_childs=True
    )
