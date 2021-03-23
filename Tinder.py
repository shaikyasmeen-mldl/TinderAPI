import firebase_admin
from firebase_admin import auth, firestore, storage, credentials

# flask packages
import flask, json, requests
from flask import abort, jsonify, request, redirect

#flask app
app = flask.Flask(__name__)



cred = credentials.Certificate("tinder-letsupgrade_file name.json")
firebase_admin.initialize_app(cred)
# Initiate firestore object
store = firestore.client()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get("email")
    uid  = ""
    msg  = ""
    try:
        user = auth.get_user_by_email(email)
        msg  = "Found the user"
        uid  = user.uid
    except:
        msg = "User not found in the firebase"
    return jsonify({"message":msg, "Response":200,"uid":uid })


@app.route('/signup', methods=['POST'])
def signUp():
    data   = request.get_json(force=True)
    email  = data.get("email")
    passwd = data.get("password")
    uid    = ""
    msg    = ""
    try:
        user = auth.create_user(email=email, email_verified=False, password=passwd)
        uid = user.uid
        msg = 'Sucessfully created new user'
    except:
        msg = "Email already used in a signup"  
    return jsonify({"uid":uid, "message":msg, "Response":200})


@app.route('/updateUser', methods=['POST'])
def updateUser():
    msg = ""
    uid = ""
    dit_user = {}
    dit = request.get_json(force=True)
    msg = "Updating user Details"
    uid = dit['uid']

    dit_user['name']      = dit['name']
    dit_user['number']    = dit['number']
    dit_user['image']     = dit['image']
    dit_user['descp']     = dit['descp']
    dit_user['dob']       = dit['dob']
    dit_user['gender']    = dit['gender']
    dit_user['passion']   = dit['passion']
    dit_user['job']       = dit['job']
    dit_user['email']     = dit['email']
    dit_user['company']   = dit['company']
    dit_user['location']  = dit['location']
    dit_user['createdAt'] = firestore.SERVER_TIMESTAMP

    store.collection("users").document(uid).set(dit_user)

    return jsonify({"uid":uid,"message":msg})
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
