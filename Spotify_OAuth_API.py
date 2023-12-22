from flask import Flask , request ,jsonify,url_for
from time import sleep
from spotipy import SpotifyOAuth ,Spotify
import requests
import time
from constant import *


app = Flask(__name__)
# Create a dictionary to store the code and token
shared_data = {
    'code': None,
    'token': None
}
@app.route('/clearsession')
def clearSession():
    shared_data['code'] = None
    shared_data['token'] = None
    return 'Code and Token Cleared'
@app.route('/redirect')
def redirectUrl():
    try:
        code = request.args.get('code', None)
        if code is None:
            return 'No Changes'
        if code == '':
            return 'Code is Empty'
        shared_data['code'] = code
        return str(shared_data['code'])
    except Exception as ex:
        return str(ex)

def sendDiscordAuthMessage():
    print('Sending Auth URL to Discord')
    content = 'Spotify Account OAuth'
    content = 'Visit URL : ' + str(SpotOAuth().get_authorize_url())
    data = {
        "username": "Spotify Bot",
        "embeds": [
            {
                "description": content,
                "title": ""
            }
        ]
    }
    result = requests.post(DISCORD_WEBHOOK_URL, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(str(err))
    else:
        print("Payload delivered successfully, code ")

def createToken():
    print('Creating New Token')
    try:
        result = {
            'status': False,
            'error': '',
        }
        sendDiscordAuthMessage()

        # Sleep and wait for the code to be set in the shared data
        timeout = 60
        starttime = time.time()
        while shared_data['code'] is None:
            if timeout <= time.time() - starttime:
                print('Code not found. Hence Unable to create new Token')
                result['error'] = 'Not Able to find Code'
                return result
            sleep(1)

        shared_data['token'] = SpotOAuth().get_access_token(shared_data['code'])
        result['status'] = True
        return result

    except Exception as ex:
        result['error'] = str(ex)
        return result

@app.route('/gettoken')
def getToken():
    Token = shared_data.get('token', None)
    if Token is not None:
        print('Token is Available')
        now = int(time.time())
        is_expired = Token['expires_at'] - now < 60
        if is_expired:
            print('Token Expired. Hence Refreshing the Token')
            Token = SpotOAuth().refresh_access_token(Token['refresh_token'])
        return jsonify(Token)
    else:
        print('Token Not Available')
        result = createToken()
        if result['status']:
            Token = shared_data.get('token', None)
            if Token is None:
                Token = {}
                Token['status'] = 400
                Token['error'] = 'Unable to Create Token'
                return jsonify(Token)
            Token['status'] = 200
            return jsonify(Token)
        else:
            Token = {}
            Token['status'] = 400
            Token['error'] = result['error']
            return jsonify(Token)

def SpotOAuth():
    return SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=url_for('redirectUrl', _external=True), scope=SCOPE)
@app.route('/')
def index():
    return str(shared_data.get('token','Nothing')) + '   :   ' + str(SpotOAuth().get_authorize_url()) + '   ::::::: ' + str(shared_data.get('code','codeNothing'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
