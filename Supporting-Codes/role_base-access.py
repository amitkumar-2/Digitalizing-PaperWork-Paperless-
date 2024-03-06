import datetime
from functools import wraps
from flask import Flask, redirect, url_for, session, render_template_string
from flask_sqlalchemy import SQLAlchemy


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@18.212.243.182/mydb1'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)

    @app.before_request
    def before_request():
        try:
            print("Current Role: ", session['role'])
        except:
            print("Current Role: Guest")

    # Define the User data-model.
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    # First Drop then Create all database tables
    # db.drop_all()
    with app.app_context():
        db.drop_all()
        db.create_all()
    # db.create_all()

    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password='Password1',
        )
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password='Password1',
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Member'))
        db.session.add(user)
        db.session.commit()

    def access_required(role="ANY"):
        """
        see: https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
        """
        def wrapper(fn):
            @wraps(fn)
            def decorated_view(*args, **kwargs):
                if session.get("role") == None or role == "ANY":
                    session['header'] = "Welcome Guest, Request a new role for higher rights!"
                    return redirect(url_for('index'))
                if session.get("role") == 'Member' and role == 'Member':
                    print("access: Member")
                    session['header'] = "Welcome to Member Page!"
                    return redirect(url_for('index'))
                if session.get("role") == 'Admin' and role == 'Admin':
                    session['header'] = "Welcome to Admin Page!"
                    print("access: Admin")
                else:
                    session['header'] = "Oh no no, you haven'tn right of access!!!"
                    return redirect(url_for('index'))
                return fn(*args, **kwargs)
            return decorated_view
        return wrapper

    # The index page is accessible to anyone
    @app.route('/')
    def index():
        print("index:", session.get("role", "nema"))
        return render_template_string('''
                <h3>{{ session["header"] if session["header"] else "Welcome Guest!" }}</h3>
                <a href="/admin_role">Get Admin Role</a> &nbsp&nbsp | &nbsp&nbsp
                <a href="/admin_page">Admin Page</a> <br><br>
                <a href="/member_role">Get Member Role</a> &nbsp&nbsp | &nbsp&nbsp
                <a href="/member_page">Member Page</a> <br><br>
                <a href="/guest_role">Get Guest Role</a> <br><br>
                <a href="/data">Try looking at DATA with different roles</a>
            ''')

    @app.route('/data')
    def data():
        return render_template_string("""
                <a href="/admin_role">Admin Role</a>
                <a href="/member_role">Member Role</a>
                <a href="/guest_role">Guest Role</a>
                <br><p>The data page will display a different context depending on the access rights.</p><br> 
                {% if not session['role'] %}
                    <h2>You must have diffrent role for access to the data.</h2>
                    <a href="{{ url_for('.index') }}">Go back?</a>
                {% endif %}

                {% if session['role'] == 'Member' or  session['role'] == 'Admin' %}
                <h2>USERS:</h2>
                <table>
                <tr>
                    <th>ID</th>
                    <th>EMAIL</th>
                </tr>
                {% for u in users %}
                <tr>
                    <td>{{ u.id }}</td>
                    <td>{{ u.email }}</td>
                </tr>
                {% endfor %}
                </table>
                {% endif %}

                {% if session['role'] == 'Admin' %}
                    <h2>ROLE:</h2>
                    <table>
                    <tr>
                        <th>ID</th>
                        <th>NAME</th>
                    </tr>
                    {% for r in roles %}
                    <tr>
                        <td>{{ r.id }}</td>
                        <td>{{ r.name }}</td>
                    </tr>
                    {% endfor %}
                    </table>

                    <h2>USER ROLES:</h2>
                    <table>
                    <tr>
                        <th>ID</th>
                        <th>USER ID</th>
                        <th>ROLE ID</th>
                    </tr>
                    {% for ur in user_roles %}
                    <tr>
                        <td>{{ ur.id }}</td>
                        <td>{{ ur.user_id }}</td>
                        <td>{{ ur.role_id }}</td>
                    </tr>
                    {% endfor %}
                    </table>
                {% endif %}
            """, 
                users=User.query, 
                roles= Role.query, 
                user_roles=UserRoles.query)

    @app.route("/member_role")
    def member_role():
        """
        Anyone can access the url and get the role of a MEMBER.
        """
        r = Role.query.get(2)
        session['role'] = r.name
        session['header'] = "Welcome to Member Access!"
        return render_template_string('<h2>{{ session["header"] }}</h2> <a href="/">Go back?</a>')

    @app.route("/member_page")
    @access_required(role="Member")
    def member_page():
        # session['header'] = "Welcome to Admin Page!"
        return render_template_string('<h1>{{ session["header"] }}</h1> <a href="/">Go back?</a>')

    @app.route("/admin_role")
    def admin_role():
        """
        Anyone can access the url and get the role of a ADMIN.
        """
        r = Role.query.get(1)
        session['role'] = r.name
        session['header'] = "Welcome to Admin Access!"
        return render_template_string('<h1>{{ session["header"] }}</h1> <a href="/">Go back?</a>')

    @app.route("/admin_page")
    @access_required(role="Admin")
    def admin_page():
        """
        This url requires an ADMIN role.
        """
        return render_template_string('<h1>{{ session["header"] }}</h1> <a href="/">Go back?</a>')

    @app.route("/guest_role")
    def guest_role():
        """
        For the GUEST, we will only delete the session and thus 'kill' the roles.
        """
        session.clear()
        return redirect(url_for('index'))

    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)