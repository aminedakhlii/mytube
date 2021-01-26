from flask import Flask , render_template , redirect , url_for, request , flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os , requests, json

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amine.db'


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(100), nullable=False)


@app.route('/remove' , methods=['POST' , 'GET'])
def remove():
    try:
        link = request.args['link']
        print(link)
        selected = Link.query.filter_by(link=link).first()
        db.session.delete(selected)
        db.session.commit()
    except:
        print(link)
    return redirect(url_for('youtube'))


@app.route('/link' , methods=['GET' , 'POST'])
def insertLink():
    url = request.form['link']
    try:
        vid = []
        if 'watch?v=' in url:
            vid = url.split('watch?v=')
        elif 'youtu.be' in url:
            vid = url.split('youtu.be/')
        finalLink = 'https://www.youtube.com/embed/' + str(vid[1].split('&')[0])
        if requests.get(finalLink).status_code != 200:
            flash('Invalid link!', 'dark')
            return redirect(url_for('youtube'))
        link = Link(link=finalLink)
        db.session.add(link)
        db.session.commit()
    except:
        flash('Invalid link !   Check your connection or enter a valid link', 'danger')
    return redirect(url_for('youtube'))

@app.route('/home')
def home():
    foldername = 'pictures'
    types = os.listdir(os.path.join(app.static_folder, foldername))
    finaltypes = []
    for type in types:
        name = type.split('.')
        finaltypes.append(name[0])
    return render_template('home.html',types=finaltypes)

@app.route('/')
def youtube():
        page = request.args.get('page' , 1 , type=int )
        links = Link.query.join().paginate(page=page , per_page=9)
        return render_template('youtube.html', links=links)

@app.route('/testapi')
def test():
    res = requests.get(
      'https://v2.api-football.com/fixtures/date/2020-07-25',
      headers= {'X-RapidAPI-Key' : 'acbd76b6a08facedc0b9db24bf29f97b'})
    with open('apiTest.json', 'w' ) as file:
        file.write(res.json())
    return res

@app.route('/default')
def default():
    res = ''
    with open('apiTest.json', 'r') as f :
        res += f.read()
    return json.dumps(res)

"""
@app.route('/random' , methods=['GET','POST'])
def random():
    foldername = 'random'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/happy')
def happy():
    foldername = 'happy'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/sad')
def sad():
    foldername = 'sad'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/tunsian')
def tunisian():
    foldername = 'tunisian'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/rap')
def rap():
    foldername = 'rap'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/arabic')
def arabic():
    foldername = 'arabic'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/faia')
def faia():
    foldername = 'faia'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/feirouz')
def feirouz():
    foldername = 'feirouz'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/kids')
def kids():
    foldername = 'kids'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)

@app.route('/virage')
def virage():
    foldername = 'virage'
    names = os.listdir(os.path.join(app.static_folder, foldername))
    return render_template('music.html',names=names, title='AmineMusic',foldername=foldername)
    """
