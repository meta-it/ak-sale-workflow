# -*- encoding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015 AKRETION (http://www.akretion.com)
#   @author Chafique DELLI
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm


class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    def _get_sub_state_selection(self, cr, uid, context=None):
        selection = super(SaleOrder, self)._get_sub_state_selection(
            cr, uid, context=context)
        selection += [
            ('waiting', 'Waiting for raw material'),
            ('ready_prod', 'Ready to be produced'),
            ('in_prod', 'In production'),
            ('ended_prod', 'Production ended'),
        ]
        return selection
