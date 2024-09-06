#3. Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.

from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize OAuth
oauth = OAuth(app)

# Configure Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_method='POST',
)

# Configure Facebook OAuth
facebook = oauth.remote_app(
    'facebook',
    consumer_key='your_facebook_app_id',
    consumer_secret='your_facebook_app_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    access_token_method='GET',
)

def get_user_info(provider, token):
    if provider == 'google':
        resp = google.get('userinfo', token=token)
    elif provider == 'facebook':
        resp = facebook.get('me?fields=id,name,email', token=token)
    return resp.data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('facebook_authorized', _external=True))

@app.route('/login/callback')
def login_callback():
    response = request.args
    if 'state' in response:
        provider = response.get('state')
        if provider == 'google':
            return google_authorized()
        elif provider == 'facebook':
            return facebook_authorized()

@app.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args.get('error_reason'),
            request.args.get('error_description')
        )
    user_info = get_user_info('google', resp['access_token'])
    session['user'] = user_info
    return redirect(url_for('profile'))

@app.route('/login/facebook/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args.get('error_reason'),
            request.args.get('error_description')
        )
    user_info = get_user_info('facebook', resp['access_token'])
    session['user'] = user_info
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)