from flask import Blueprint, jsonify, request 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity 
from app import db  # On importe db pour les sessions et les commits
from app.models import User, Role
from sqlalchemy import select # Import nécessaire pour la syntaxe moderne de requête

# Définition du Blueprint avec le préfixe /auth
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# --- TÂCHE S1.2 : INSCRIPTION (/register) ---
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"msg": "Email et mot de passe requis."}), 400

    # 1. Vérification de l'existence (Syntaxe robuste pour le contexte Flask Factory)
    stmt = select(User).filter_by(email=email)
    if db.session.execute(stmt).scalars().first():
        return jsonify({"msg": "L'utilisateur existe déjà."}), 409
    
    # 2. Récupération ou création du rôle 'user' par défaut
    default_role = db.session.execute(select(Role).filter_by(name='user')).scalars().first()
    if not default_role:
        # Si le rôle n'existe pas (ce qui ne devrait pas arriver si la BDD est initialisée)
        return jsonify({"msg": "Rôle 'user' manquant. Initialisez la BDD."}), 500
    
    # 3. Création et hachage
    new_user = User(email=email, role_id=default_role.id)
    new_user.set_password(password) # Utilise l'extension Bcrypt via le modèle
    
    # 4. Enregistrement
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Inscription réussie", "user_id": new_user.id}), 201


# --- TÂCHE S1.3 : CONNEXION (/login) ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email et mot de passe requis."}), 400

    # 1. Récupération de l'utilisateur (Syntaxe robuste)
    stmt = select(User).filter_by(email=email)
    user = db.session.execute(stmt).scalars().first()

    # 2. Vérification de l'existence et du mot de passe
    if user and user.check_password(password):
        
        # 3. Création du Jeton JWT
        # L'identité est l'ID de l'utilisateur
        access_token = create_access_token(identity=str(user.id)) 
        
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Email ou mot de passe invalide"}), 401


# --- TÂCHE S1.4 : ROUTE PROTÉGÉE (/protected) ---
@auth_bp.route('/protected', methods=['GET'])
@jwt_required() # Force la vérification d'un Jeton JWT valide
def protected():
    # Récupère l'ID de l'utilisateur à partir du jeton vérifié
    current_user_id = get_jwt_identity()
    
    # On récupère les infos complètes pour la réponse (moins sujet à erreur avec .get())
    user = db.session.get(User, current_user_id)
    
    if not user:
        return jsonify({"msg": "Utilisateur non trouvé dans la base de données."}), 404
    
    return jsonify({
        "msg": f"Accès autorisé pour l'utilisateur ID: {current_user_id}",
        "email": user.email,
        "role_id": user.role_id
    }), 200