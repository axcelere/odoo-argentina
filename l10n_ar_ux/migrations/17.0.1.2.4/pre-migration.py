from openupgradelib import openupgrade
import logging

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'l10n_ar_ux.report_invoice_document',
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

    env.ref('l10n_ar.report_invoice_document', raise_if_not_found=False).write({
        'arch_base': """
        <data inherit_id="account.report_invoice_document" primary="True">
        <!-- custom header and footer -->
        <t t-set="o" position="after">
            <t t-set="custom_header" t-value="'l10n_ar.custom_header'"/>
            <t t-set="report_date" t-value="o.invoice_date"/>
            <t t-set="report_number" t-value="o.l10n_latam_document_number"/>
            <t t-set="pre_printed_report" t-value="report_type == 'pdf' and o.journal_id.l10n_ar_afip_pos_system == 'II_IM'"/>
            <t t-set="document_letter" t-value="o.l10n_latam_document_type_id.l10n_ar_letter"/>
            <t t-set="document_legend" t-value="o.l10n_latam_document_type_id.code and 'Cod. %02d' % int(o.l10n_latam_document_type_id.code) or ''"/>
            <t t-set="report_name" t-value="o.l10n_latam_document_type_id.report_name"/>
            <t t-set="header_address" t-value="o.journal_id.l10n_ar_afip_pos_partner_id"/>

            <t t-set="custom_footer">
                <div class="row">
                    <div name="footer_left_column" class="col-8 text-start">
                    </div>
                    <div name="footer_right_column" class="col-4 text-end">
                        <div name="pager" t-if="report_type == 'pdf'">
                            Page: <span class="page"/> / <span class="topage"/>
                        </div>
                    </div>
                </div>
            </t>
            <t t-set="fiscal_bond" t-value="o.journal_id.l10n_ar_afip_pos_system in ['BFERCEL', 'BFEWS']"/>
        </t>

        <!-- remove default partner address -->
        <t t-set="address" position="replace"/>
        <xpath expr="//div[@name='address_not_same_as_shipping']" position="replace">
            <div name="address_not_same_as_shipping"/>
        </xpath>
        <xpath expr="//div[@name='address_same_as_shipping']" position="replace">
            <div name="address_same_as_shipping"/>
        </xpath>
        <xpath expr="//div[@name='no_shipping']" position="replace">
            <div name="no_shipping"/>
        </xpath>

        <!-- remove default document title -->
        <h2 position="replace"/>

        <!-- NCM column for fiscal bond -->
        <th name="th_description" position="after">
            <th t-if="fiscal_bond" name="th_ncm_code" class="text-start"><span>NCM</span></th>
        </th>
        <td name="account_invoice_line_name" position="after">
            <td t-if="fiscal_bond" name="ncm_code"><span t-field="line.product_id.l10n_ar_ncm_code"/></td>
        </td>

        <!-- use latam prices (to include/exclude VAT) -->
        <t t-set="current_subtotal" t-value="current_subtotal + line.price_subtotal" position="before">
            <t t-set="l10n_ar_values" t-value="line._l10n_ar_prices_and_taxes()"/>
        </t>
        <xpath expr="//span[@t-field='line.price_unit']" position="attributes">
            <attribute name="t-field"></attribute>
            <attribute name="t-out">l10n_ar_values['price_unit']</attribute>
            <attribute name="t-options">{"widget": "monetary", "display_currency": o.currency_id}</attribute>
        </xpath>
        <t t-set="current_subtotal" t-value="current_subtotal + line.price_subtotal" position="attributes">
            <attribute name="t-value">current_subtotal + l10n_ar_values['price_subtotal']</attribute>
        </t>
        <!-- if b2c we still wants the latam subtotal -->
        <t t-set="current_total" t-value="current_total + line.price_total" position="attributes">
            <attribute name="t-value">current_subtotal + l10n_ar_values['price_subtotal']</attribute>
        </t>
        <!-- label amount for subtotal column on b2b and b2c -->
        <xpath expr="//th[@name='th_subtotal']/span" position="replace">
            <span>Amount</span>
        </xpath>
        <span t-field="line.price_subtotal" position="attributes">
            <attribute name="t-field"></attribute>
            <attribute name="t-out">l10n_ar_values['price_subtotal']</attribute>
            <attribute name="t-options">{"widget": "monetary", "display_currency": o.currency_id}</attribute>
        </span>

        <t t-set="tax_totals" position="attributes">
            <attribute name="t-value">o._l10n_ar_get_invoice_totals_for_report()</attribute>
        </t>

        <!-- use column vat instead of taxes and only if vat discriminated -->
        <xpath expr="//th[@name='th_taxes']/span" position="replace">
            <span>% VAT</span>
        </xpath>

        <!-- use column vat instead of taxes and only list vat taxes-->
        <xpath expr="//th[@name='th_taxes']" position="attributes">
            <attribute name="t-if">not o._l10n_ar_include_vat()</attribute>
        </xpath>
        <xpath expr="//span[@id='line_tax_ids']/.." position="attributes">
            <attribute name="t-if">not o._l10n_ar_include_vat()</attribute>
        </xpath>
        <span id="line_tax_ids" position="attributes">
            <attribute name="t-out">', '.join(map(lambda x: (x.invoice_label or x.name), line.tax_ids.filtered(lambda x: x.tax_group_id.l10n_ar_vat_afip_code)))</attribute>
        </span>

        <!-- remove payment reference that is not used in Argentina -->
        <xpath expr="//span[@t-field='o.payment_reference']/../.." position="replace"/>

        <!-- replace information section and usage argentinean style -->
        <div id="informations" position="replace">
            <div id="informations" class="row mt8 mb8">
                <div class="col-6">

                    <!-- IDENTIFICACION (ADQUIRIENTE-LOCATARIO-PRESTARIO) -->

                    <!-- (14) Apellido uy Nombre: Denominicacion o Razon Soclial -->
                    <strong>Customer: </strong><span t-field="o.partner_id.commercial_partner_id.name"/>

                    <!-- (15) Domicilio Comercial -->
                    <br/>
                    <span t-field="o.partner_id" t-options="{'widget': 'contact', 'fields': ['address'], 'no_marker': true, 'no_tag_br': True}"/>

                    <!-- (16) Responsabilidad AFIP -->
                    <strong>VAT Cond: </strong><span t-field="o.partner_id.l10n_ar_afip_responsibility_type_id"/>

                    <!-- (17) CUIT -->
                    <t t-if="o.partner_id.vat and o.partner_id.l10n_latam_identification_type_id and o.partner_id.l10n_latam_identification_type_id.l10n_ar_afip_code != '99'">
                        <br/><strong><t t-out="o.partner_id.l10n_latam_identification_type_id.name or o.company_id.account_fiscal_country_id.vat_label" id="inv_tax_id_label"/>:</strong> <span t-out="o.partner_id.l10n_ar_formatted_vat if o.partner_id.l10n_ar_vat else o.partner_id.vat"/>
                    </t>

                </div>
                <div class="col-6">

                    <t t-if="o.invoice_date_due">
                        <strong>Due Date: </strong>
                        <span t-field="o.invoice_date_due"/>
                    </t>

                    <t t-if="o.invoice_payment_term_id" name="payment_term">
                        <br/><strong>Payment Terms: </strong><span t-field="o.invoice_payment_term_id.name"/>
                    </t>

                    <t t-if="o.invoice_origin">
                        <br/><strong>Source:</strong>
                        <span t-field="o.invoice_origin"/>
                    </t>

                    <t t-if="o.ref">
                        <br/><strong>Reference:</strong>
                        <span t-field="o.ref"/>
                    </t>

                    <!-- (18) REMITOS -->
                    <!-- We do not have remitos implement yet. print here the remito number when we have it -->

                    <t t-if="o.invoice_incoterm_id">
                        <br/>
                        <strong>Incoterm:</strong>
                        <p t-if="o.incoterm_location">
                            <span t-field="o.invoice_incoterm_id.code"/> <br/>
                            <span t-field="o.incoterm_location"/>
                        </p>
                        <p t-else="" t-field="o.invoice_incoterm_id.name" class="m-0"/>
                    </t>

                </div>

            </div>
        </div>

        <xpath expr="//div[@id='payment_term']" position="before">
            <div class="mb-4">
                <t t-if="o.l10n_ar_afip_concept in ['2', '3', '4'] and o.l10n_ar_afip_service_start and o.l10n_ar_afip_service_end">
                    <strong>Invoiced period: </strong><span t-field="o.l10n_ar_afip_service_start"/> to <span t-field="o.l10n_ar_afip_service_end"/>
                </t>
                <t t-if="o.currency_id != o.company_id.currency_id">
                    <br/><strong>Currency: </strong><span t-out="'%s - %s' % (o.currency_id.name, o.currency_id.currency_unit_label)"/>
                    <br/><strong>Exchange rate: </strong> <span t-field="o.l10n_ar_currency_rate"/>
                </t>
                <!-- Show CBU for FACTURA DE CREDITO ELECTRONICA MiPyMEs and NOTA DE DEBITO ELECTRONICA MiPyMEs -->
                <t t-if="o.l10n_latam_document_type_id.code in ['201', '206', '211', '202', '207', '212'] and o.partner_bank_id">
                    <br/><strong>CBU for payment: </strong><span t-out="o.partner_bank_id.acc_number or '' if o.partner_bank_id.acc_type == 'cbu' else ''"/>
                </t>

            </div>
        </xpath>

        <!-- Show total amount in letters for MiPyMEs document types according to the law
         http://biblioteca.afip.gob.ar/dcp/LEY_C_027440_2018_05_09 article 5.f -->
        <xpath expr="//div[@id='total']/div/table" position="after">
            <t t-if="o.l10n_latam_document_type_id.code in ['201', '202', '203', '206', '207', '208', '211', '212', '213']">
                <strong>Son: </strong><span t-out="o.currency_id.with_context(lang='es_AR').amount_to_text(o.amount_total)"/>
            </t>
        </xpath>

        <!-- RG 5003: Add legend for 'A' documents that have a Monotribuista receptor -->
        <div name="comment" position="after">
            <p t-if="o.partner_id.l10n_ar_afip_responsibility_type_id.code in ['6', '13'] and o.l10n_latam_document_type_id.l10n_ar_letter == 'A'" >
                The tax credit specified in this voucher may only be computed for purposes of the Tax Support and Inclusion Regime for Small Taxpayers of Law No. 27,618.
            </p>
        </div>

        <t t-call="account.document_tax_totals" position="attributes">
            <attribute name="t-call">l10n_ar.document_tax_totals</attribute>
        </t>
        </data>
        """
    })
