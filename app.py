import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from api.requests_api import RequestsApi
from models.Vote import Vote
import random

app = Flask(__name__)
app.secret_key = "655rf677y8989y"

def session_validate():
    if 'login' in session:
        return True
    else:
        return False
        


@app.route('/')
def index():
    if session_validate() == False:
        return redirect(url_for('login'))
        
    res = RequestsApi.get_all_api()
    # print(res)
    return render_template('index.htm', votes=res)


@app.route('/new')
def new():
    if session_validate() == False:
        return redirect(url_for('login'))
    return render_template('create.htm')


@app.route('/save', methods=['POST'])
def save():
    if session_validate() == False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            imglist = ['ld0', 'cvr', 'ar9', 'djk', 'lnk', '9bf']
            img = random.choice(imglist)

            value_input = request.form['value_input']

            vote = Vote(value=int(value_input), image_id=img)
            res = RequestsApi.save_api(vote)
            flash('Vote saved')
            return redirect(url_for('index'))
            
            # print(res)
        except:
            flash('No saved')


@app.route('/view/<id>')
def view(id):
    if session_validate() == False:
        return redirect(url_for('login'))
    res = RequestsApi.get_one_api(id)
    # print(res)
    return render_template('view.htm', vote = res)


@app.route('/delete/<id>')
def delete(id):
    if session_validate() == False:
        return redirect(url_for('login'))
    res = RequestsApi.delete_api(id)
    flash('Deleted')
    return redirect(url_for('index'))



@app.route('/login', methods=['POST', 'GET'])
def login():
    if session_validate() == True:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            if (username == 'Camilo' and password == '123456'):
                session['login'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('User not found')
        except:
            flash('Connection Error')

    return render_template('login.htm')

@app.route('/logout')
def logout():
    if session_validate() == False:
        return redirect(url_for('login'))
    session.pop('login', None)
    session.pop('username', None)

    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(port=8085, debug=True)
