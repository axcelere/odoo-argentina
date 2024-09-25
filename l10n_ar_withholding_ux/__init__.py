from . import models
from . import wizards
from odoo.addons.l10n_ar_withholding import demo

from odoo.addons.l10n_ar_withholding.models.account_payment import AccountPayment

import logging

_logger = logging.getLogger(__name__)



def monkey_patch_synchronize_to_moves():

    def _synchronize_to_moves(self, changed_fields):
        return super(AccountPayment, self)._synchronize_to_moves(changed_fields)
    AccountPayment._synchronize_to_moves = _synchronize_to_moves
