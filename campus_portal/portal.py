"""Implementación intencionalmente insegura del portal académico."""

from campus_portal.data import AUDIT_LOG, UPLOADS, USERS


class CampusPortal:
    """Portal con decisiones de diseño débiles para uso didáctico."""

    def login(self, username, password):
        user = USERS.get(username)
        if user is None:
            return {
                "ok": False,
                "error": f"El usuario {username} no existe",
            }

        if user["password"] != password:
            return {
                "ok": False,
                "error": f"La contraseña de {username} no coincide",
            }

        return {
            "ok": True,
            "message": "Inicio de sesión correcto",
            "user": {
                "username": username,
                "role": user["role"],
                "email": user["email"],
                "password": user["password"],
            },
            "debug": {
                "known_roles": ["student", "teacher", "admin"],
            },
        }

    def change_role(self, actor, target, new_role):
        if target not in USERS:
            return {"ok": False, "error": f"No existe el usuario {target}"}

        old_role = USERS[target]["role"]
        USERS[target]["role"] = new_role
        return {
            "ok": True,
            "message": f"{actor} cambió el rol de {target}",
            "before": old_role,
            "after": new_role,
            "user_state": USERS[target],
        }

    def upload_attachment(self, actor, filename, content_type, size):
        file_record = {
            "owner": actor,
            "filename": filename,
            "content_type": content_type,
            "size": size,
            "public_url": f"/uploads/{filename}",
            "review_status": "pending",
        }
        UPLOADS.append(file_record)
        return {"ok": True, "file": file_record}

    def review_upload(self, actor, index, review_status):
        upload = UPLOADS[index]
        upload["review_status"] = review_status
        upload["reviewed_by"] = actor
        return {"ok": True, "file": upload}

    def get_security_dashboard(self, actor):
        return {
            "ok": True,
            "requested_by": actor,
            "users": USERS,
            "uploads": UPLOADS,
            "audit_log": AUDIT_LOG,
        }
