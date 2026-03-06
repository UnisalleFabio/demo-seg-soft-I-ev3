"""Implementación con principios de diseño seguro para el EV3."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import os
import re

from campus_portal.data import build_users, hash_password


@dataclass(frozen=True)
class SecuritySettings:
    # Principio: seguridad por defecto. El sistema inicia en modo conservador.
    debug_mode: bool = False
    max_upload_size: int = 2_000_000
    allowed_upload_types: tuple[str, ...] = (
        "application/pdf",
        "image/png",
        "image/jpeg",
    )


# Principio: privilegio mínimo. Cada rol recibe solo las acciones que necesita.
PERMISSIONS = {
    "student": frozenset({"login", "upload_attachment", "view_profile"}),
    "teacher": frozenset({"login", "review_upload", "view_profile"}),
    "admin": frozenset({"login", "change_role", "read_audit_log", "view_profile"}),
}


@dataclass
class AuditEvent:
    timestamp: str
    actor: str
    action: str
    status: str
    detail: str


class CampusPortal:
    """Portal pequeño que aplica principios de diseño seguro."""

    def __init__(self, settings: SecuritySettings | None = None):
        # Principio: seguridad por diseño. La política de seguridad se define
        # como parte del servicio y no como un parche externo posterior.
        self.settings = settings or SecuritySettings()
        self.users = build_users()
        self.uploads = []
        self.audit_log: list[AuditEvent] = []
        self.failed_logins: dict[str, int] = {}

    def login(self, username: str, password: str):
        actor = username or "anonymous"
        user = self.users.get(username)
        attempted_hash = hash_password(password)

        # Principio: falla segura. Si no podemos validar credenciales, negamos.
        if user is None or attempted_hash != user["password_hash"]:
            self._track_failed_login(actor)
            return {"ok": False, "error": "Operación rechazada"}

        self.failed_logins[actor] = 0
        self._record_audit(actor, "login", "allowed", "Inicio de sesión exitoso")
        return {
            "ok": True,
            # Principio: validación de salidas. No exponemos hash ni debug.
            "user": self._public_user_view(username),
        }

    def change_role(self, actor: str, target: str, new_role: str):
        # Principio: separación de responsabilidades. Solo admin cambia roles
        # y no permitimos autopromoción como atajo de control.
        denial = self._require_permission(actor, "change_role")
        if denial:
            return denial
        if actor == target:
            return self._deny(actor, "change_role", "No se permite autopromoción")
        if target not in self.users or new_role not in PERMISSIONS:
            return self._deny(actor, "change_role", "Solicitud de cambio inválida")

        old_role = self.users[target]["role"]
        self.users[target]["role"] = new_role
        self._record_audit(
            actor,
            "change_role",
            "allowed",
            f"Rol de {target} cambiado de {old_role} a {new_role}",
        )
        return {
            "ok": True,
            "message": "Cambio de rol aplicado",
            "target": target,
            "before": old_role,
            "after": new_role,
        }

    def upload_attachment(self, actor: str, filename: str, content_type: str, size: int):
        denial = self._require_permission(actor, "upload_attachment")
        if denial:
            return denial
        validation_error = self._validate_upload(filename, content_type, size)
        if validation_error:
            return self._deny(actor, "upload_attachment", validation_error)

        file_record = {
            "owner": actor,
            "stored_as": self._sanitize_filename(filename),
            "content_type": content_type,
            "size": size,
            "review_status": "pending",
        }
        self.uploads.append(file_record)
        self._record_audit(actor, "upload_attachment", "allowed", file_record["stored_as"])
        return {
            "ok": True,
            # Principio: validación de salidas. No exponemos ruta pública directa.
            "file": self._public_upload_view(file_record),
        }

    def review_upload(self, actor: str, index: int, review_status: str):
        denial = self._require_permission(actor, "review_upload")
        if denial:
            return denial
        if index < 0 or index >= len(self.uploads):
            return self._deny(actor, "review_upload", "Archivo inexistente")
        if review_status not in {"approved", "rejected"}:
            return self._deny(actor, "review_upload", "Estado de revisión inválido")

        upload = self.uploads[index]
        upload["review_status"] = review_status
        upload["reviewed_by"] = actor
        self._record_audit(actor, "review_upload", "allowed", f"Revisión {review_status}")
        return {"ok": True, "file": self._public_upload_view(upload)}

    def get_security_dashboard(self, actor: str):
        denial = self._require_permission(actor, "read_audit_log")
        if denial:
            return denial

        # Principio: auditoría y monitoreo continuo. El dashboard resume
        # eventos relevantes sin exponer datos sensibles de usuarios.
        failed_logins = len(
            [event for event in self.audit_log if event.action == "login" and event.status == "denied"]
        )
        suspicious_events = len(
            [event for event in self.audit_log if "sospechoso" in event.detail.lower()]
        )
        return {
            "ok": True,
            "summary": {
                "users": len(self.users),
                "uploads": len(self.uploads),
                "failed_logins": failed_logins,
                "suspicious_events": suspicious_events,
            },
            "audit_log": [asdict(event) for event in self.audit_log],
        }

    def _require_permission(self, actor: str, action: str):
        user = self.users.get(actor)
        # Principio: seguridad por defecto. Si no existe permiso explícito,
        # negamos la operación.
        if user is None:
            return self._deny(actor, action, "Actor desconocido")
        role = user["role"]
        allowed_actions = PERMISSIONS.get(role, frozenset())
        if action not in allowed_actions:
            return self._deny(actor, action, "Operación no autorizada")
        return None

    def _validate_upload(self, filename: str, content_type: str, size: int):
        # Principio: validación de entradas y salidas. El archivo se valida por
        # nombre, tipo y tamaño antes de aceptarse.
        if not filename or len(filename) > 80:
            return "Nombre de archivo inválido"
        if content_type not in self.settings.allowed_upload_types:
            # Principio: minimización de superficie de ataque. Solo aceptamos
            # tipos de archivo necesarios para el caso de negocio.
            return "Tipo de archivo no permitido"
        if size <= 0 or size > self.settings.max_upload_size:
            return "Tamaño de archivo no permitido"
        return None

    def _sanitize_filename(self, filename: str):
        safe_name = os.path.basename(filename)
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", safe_name)
        return safe_name

    def _public_user_view(self, username: str):
        user = self.users[username]
        return {
            "username": username,
            "role": user["role"],
            "email": user["email"],
        }

    def _public_upload_view(self, file_record: dict):
        return {
            "owner": file_record["owner"],
            "stored_as": file_record["stored_as"],
            "content_type": file_record["content_type"],
            "size": file_record["size"],
            "review_status": file_record["review_status"],
            "reviewed_by": file_record.get("reviewed_by"),
        }

    def _record_audit(self, actor: str, action: str, status: str, detail: str):
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor=actor,
            action=action,
            status=status,
            detail=detail,
        )
        self.audit_log.append(event)

    def _track_failed_login(self, actor: str):
        # Principio: auditoría y monitoreo continuo. Registramos fallos y
        # elevamos una alerta simple cuando hay repetición sospechosa.
        attempts = self.failed_logins.get(actor, 0) + 1
        self.failed_logins[actor] = attempts
        detail = "Credenciales inválidas"
        if attempts >= 3:
            detail = "Patrón de login sospechoso"
        self._record_audit(actor, "login", "denied", detail)

    def _deny(self, actor: str, action: str, detail: str):
        # Principio: falla segura. Rechazamos la operación y registramos el
        # motivo sin exponer detalles internos en la respuesta pública.
        self._record_audit(actor, action, "denied", detail)
        return {"ok": False, "error": "Operación rechazada"}
