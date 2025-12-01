from app.models import User



def test_password_hashing():
    user = User(email='test@email.com',role_id=1)
    password_clair = 'securepassword'
    user.set_password(password_clair)


    # verifier que le hash a bien ete genere
    assert user.password_hash is not None
    assert len(user.password_hash) > 50 #le hash bcrypt est long

    # verifier la correspondance du mot de passe

    assert user.check_password(password_clair) is True

    # verifier un mot de passe incorrect
    assert user.check_password('wrongpassword') is False