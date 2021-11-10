{
    'name': 'Argentinian Accounting UX',
    'version': "13.0.1.28.2",
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'account_debit_note',
        'l10n_ar',
        'account_check',
        # for payment group report
        'account_withholding',
        'account_payment_group_document',
    ],
    'data': [
        'data/res_currency_data.xml',
        'data/account_account_tag_data.xml',
        'data/account_tax_group_data.xml',
        # 'data/account_chart_template_data.xml',
        'data/account_tax_template_data.xml',
        'wizards/account_move_change_rate_views.xml',
        'views/portal_templates.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/afip_concept_view.xml',
        'views/afip_activity_view.xml',
        'views/afip_tax_view.xml',
        'views/report_invoice.xml',
        'reports/report_account_transfer.xml',
        # 'views/account_payment_view.xml',
        'views/account_journal_views.xml',
        'views/ir_actions_views.xml',
        'wizards/res_config_settings_views.xml',
        'reports/account_invoice_report_view.xml',
        # 'reports/report_payment_group.xml',
        'security/ir.model.access.csv',
        'security/l10n_ar_ux_security.xml',
        'data/res_groups_data.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
