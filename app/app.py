from flask import Flask, render_template, send_file

app = Flask(__name__, static_url_path='')

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/companies.html')
def companies():
    return render_template('companies.html')

@app.route('/company.html')
def company():
    return render_template('company.html')

@app.route('/company1.html')
def company1():
    return render_template('company1.html')

@app.route('/game1.html')
def game1():
    return render_template('game1.html')

@app.route('/game2.html')
def game2():
    return render_template('game2.html')

@app.route('/game3.html')
def game3():
    return render_template('game3.html')

@app.route('/games.html')
def games():
    return render_template('games.html')

@app.route('/people.html')
def people():
    return render_template('people.html')

@app.route('/person1.html')
def person1():
    return render_template('person1.html')

@app.route('/person2.html')
def person2():
    return render_template('person2.html')

@app.route('/person3.html')
def person3():
    return render_template('person3.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
