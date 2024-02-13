from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/home/ayub/Documents/EcoConnect/ecoconnect-65919-firebase-adminsdk-vtevx-c04bed39af.json') 
firebase_admin.initialize_app(cred)
db = firestore.client()

# Home route (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Login/Signup route
@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html')

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    country = request.form['country']
    town = request.form['town']
    try:
        user = auth.create_user(email=email, password=password)
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'email': email,
            'username': username,
            'country': country,
            'town': town
        })
        return redirect(url_for('login_signup'))
    except Exception as e:
        return str(e)

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.get_user_by_email(email)
        # Add login logic here, such as session management
        return render_template('dashboard.html')
    except Exception as e:
        return str(e)

# Resource sharing route
@app.route('/resources')
def resources():
    # Retrieve resource data from Firestore
    # Render template with resource data
    return render_template('resources.html')

# Event management route
@app.route('/events')
def events():
    # Retrieve event data from Firestore
    # Render template with event data
    return render_template('events.html')

# Community discussions route
@app.route('/discussions')
def discussions():
    # Retrieve discussion data from Firestore
    # Render template with discussion data
    return render_template('discussions.html')

if __name__ == '__main__':
    app.run(debug=True)
