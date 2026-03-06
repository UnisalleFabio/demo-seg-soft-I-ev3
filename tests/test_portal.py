"""Pruebas básicas para la implementación segura."""

import unittest

from campus_portal.portal import CampusPortal


class CampusPortalTests(unittest.TestCase):
    def test_login_uses_generic_error(self):
        portal = CampusPortal()
        response = portal.login("desconocido", "123")
        self.assertFalse(response["ok"])
        self.assertEqual(response["error"], "Operación rechazada")

    def test_student_cannot_change_own_role(self):
        portal = CampusPortal()
        response = portal.change_role("ana", "ana", "admin")
        self.assertFalse(response["ok"])
        self.assertEqual(portal.users["ana"]["role"], "student")

    def test_upload_rejects_disallowed_type(self):
        portal = CampusPortal()
        response = portal.upload_attachment("ana", "script.sh", "text/x-shellscript", 200)
        self.assertFalse(response["ok"])
        self.assertEqual(len(portal.uploads), 0)

    def test_admin_can_read_audit_dashboard(self):
        portal = CampusPortal()
        portal.login("ana", "123456")
        response = portal.get_security_dashboard("root")
        self.assertTrue(response["ok"])
        self.assertIn("summary", response)


if __name__ == "__main__":
    unittest.main()
