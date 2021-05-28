# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_register_payment(self):
        self.ensure_one()
        return {
            "name": _("Register Payment"),
            "res_model": "sale.payment.register",
            "view_mode": "form",
            "context": {
                "active_model": "sale.order",
                "active_id": self.id,
                "active_ids": self.ids,
            },
            "target": "new",
            "type": "ir.actions.act_window",
        }

    payment_line_ids = fields.One2many(
        "account.move.line",
        "sale_id",
        string="Payments Entries",
        domain=[
            ("account_id.internal_type", "=", "receivable"),
            ("move_id.state", "!=", "cancel"),
        ],
        copy=False,
    )
    amount_down_payment = fields.Monetary(
        compute="_compute_amount_down_payment", string="Down Payment Amount"
    )
    # amount_residual : only used to hide 'Register Payment' button
    amount_residual = fields.Monetary(
        compute="_compute_amount_down_payment", string="Residual"
    )

    @api.depends(
        "payment_line_ids.credit",
        "payment_line_ids.debit",
        "payment_line_ids.amount_currency",
        "payment_line_ids.currency_id",
        "payment_line_ids.date",
        "currency_id",
    )
    def _compute_amount_down_payment(self):
        for sale in self:
            # Avoid failure on creation since currency_id is related to mandatory field
            if not sale.currency_id:
                sale.amount_down_payment = 0.0
                sale.amount_residual = 0.0
                continue
            down_payment = 0.0
            sale_currency = sale.currency_id
            if sale_currency == sale.company_id.currency_id:
                for pl in sale.payment_line_ids:
                    down_payment -= pl.balance
            else:
                for pl in sale.payment_line_ids:
                    if (
                        pl.currency_id
                        and pl.currency_id == sale_currency
                        and pl.amount_currency
                    ):
                        down_payment -= pl.amount_currency
                    else:
                        down_payment -= sale.company_id.currency_id._convert(
                            pl.balance, sale_currency, sale.company_id, pl.date
                        )
            down_payment = float_round(
                down_payment, precision_rounding=sale.currency_id.rounding
            )
            sale.amount_down_payment = down_payment
            sale.amount_residual = float_round(
                sale.amount_total - down_payment,
                precision_rounding=sale.currency_id.rounding,
            )

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if not vals.get("payment_reference"):
            vals["payment_reference"] = self.name
        return vals
