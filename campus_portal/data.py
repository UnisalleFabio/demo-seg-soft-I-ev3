"""Datos en memoria para el ejemplo guiado seguro."""

import hashlib


def hash_password(raw_password):
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def build_users():
    return {
        "ana": {
            "password_hash": hash_password("123456"),
            "role": "student",
            "email": "ana@campus.local",
        },
        "luis": {
            "password_hash": hash_password("docente123"),
            "role": "teacher",
            "email": "luis@campus.local",
        },
        "root": {
            "password_hash": hash_password("admin"),
            "role": "admin",
            "email": "root@campus.local",
        },
    }
