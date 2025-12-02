from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User
from app import db
from sqlalchemy import select


# Décorateur pour vérifier le rôle de l'utilisateur
def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # ensure we use the DB instance from the package `app` (single instance)
            from flask import current_app
            user_id_raw = get_jwt_identity()
            # Debug information to ensure that the current_app is registered with db
            try:
                current_app.logger.debug('Role check: current_app id=%s db.engines=%s', id(current_app), list(db.engines.keys()))
            except Exception:
                pass
            try:
                user_id = int(user_id_raw) if user_id_raw is not None else None
            except (TypeError, ValueError):
                user_id = user_id_raw

            user = db.session.get(User, user_id)

            if user and user.role.name in roles:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": "Accès refusé : rôle insuffisant."}), 403
        return decorator
    return wrapper