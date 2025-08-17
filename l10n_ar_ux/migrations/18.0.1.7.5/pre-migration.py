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

    # NO EXISTE MAS ESE TAG POR LO QUE DEBE SER LIMPIADO
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_924'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_923'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_922'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real

    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_919'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_904'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_902'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real
    tag_xml_id = 'l10n_ar_ux.tag_tax_jurisdiccion_901'
    try:
        tag = env.ref(tag_xml_id)
    except ValueError:
        tag = None

    if tag:
        # Buscar todas las repartition lines que referencian este tag
        repartition_lines = env['account.tax.repartition.line'].search([
            ('tag_ids', 'in', [tag.id])
        ])

        if repartition_lines:
            for repartition in repartition_lines:
                # Sacar el tag de las líneas (sin borrar la línea entera)
                repartition.tag_ids = [(3, tag.id)]
            env.cr.commit()  # importante si quieres asegurarte que se aplica antes del upgrade real

    cr.execute("""
        DELETE FROM account_account_tag_account_move_line_rel
        WHERE account_account_tag_id IN (24,41,44,37,36,35,33,29,28,22,21)
    """)
    cr.execute("""
        DELETE FROM account_account_tag_account_tax_repartition_line_rel
        WHERE account_account_tag_id IN (24,41,44,40,38,37,36,35,34,33,32,31,30,29,28,27,26,25,23,22)
    """)
    cr.execute("""
        DELETE FROM res_partner_arba_alicuot
        WHERE tag_id IN (41)
    """)
    env.cr.commit()

    view = env.ref("stock_ux.product_form_view_procurement_button", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("stock_ux.product_template_form_view_procurement_button", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_stock.product_template_form_view", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_stock.product_uom_form_view", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_stock.product_uom_tree_view", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_stock.product_uom_categ_form_view", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_account_withholding.res_config_settings_view_form", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("l10n_ar_account_withholding.view_account_payment_form", raise_if_not_found=False)
    if view:
        view.unlink()

    env.cr.commit()
