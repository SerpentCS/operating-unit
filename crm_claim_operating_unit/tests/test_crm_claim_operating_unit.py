# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


class TestCrmClaimOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.crm_claim_model = self.env['crm.claim']

        self.company = self.env.ref('base.main_company')
        self.partner = self.env.ref('base.res_partner_1')
        self.grp_sale_manager = self.env.ref('base.group_sale_manager')

        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')

        self.user1 = self._create_user('user_1',
                                       [self.grp_sale_manager],
                                       self.company,
                                       [self.ou1, self.b2c])
        self.user2 = self._create_user('user_2',
                                       [self.grp_sale_manager],
                                       self.company,
                                       [self.b2c])

        self.crm_claim1 = self._create_crm_claim(self.user1.id, self.ou1)

        self.crm_claim2 = self._create_crm_claim(self.user2.id, self.b2c)

    def _create_user(self, login, groups, company, operating_units,
                     context=None):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test HR User',
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_crm_claim(self, uid, operating_unit):
        """Creates a CRM Claim."""
        claim = self.crm_claim_model.sudo(uid).create({
            'name': " Damaged Products ",
            'operating_unit_id': operating_unit.id,
            'partner_id': self.partner.id,
            'user_id': uid,
            })
        return claim

    def test_security(self):
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Claims of Main Operating Unit.
        record = self.crm_claim_model.sudo(self.user2.id).search(
                                          [('id', '=', self.crm_claim1.id),
                                           ('operating_unit_id', '=',
                                           self.ou1.id)])
        self.assertEqual(record.ids, [], 'User 2 should not have access to '
                         '%s' % self.ou1.name)
