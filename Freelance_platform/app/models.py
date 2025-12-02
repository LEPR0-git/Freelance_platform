from app import db, bcrypt


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    profile_rel = db.relationship('Profile', backref='user', uselist=False)

    def set_password(self, password):
        hashed = bcrypt.generate_password_hash(password)
        self.password_hash = hashed.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    is_freelancer = db.Column(db.Boolean, default=False)

    # cle etrangere vers user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # relation Bidirectionnel 
    user = db.relationship('User',backref=db.backref('profile', uselist=False))

    def __repr__(self):
        return f'<Profile {self.full_name}>'