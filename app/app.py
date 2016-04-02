from flask import Flask, render_template, send_file

app = Flask(__name__, static_url_path='')

@app.route('/index.html')
@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/about.html')
def about():
    return send_file('templates/about.html')

@app.route('/companies.html')
def companies():
    return send_file('templates/companies.html')

@app.route('/company.html')
def company():
    return send_file('templates/company.html')

@app.route('/company1.html')
def company1():
    return send_file('templates/company1.html')

@app.route('/company2.html')
def company2():
    return send_file('templates/company2.html')

@app.route('/company3.html')
def company3():
    return send_file('templates/company3.html')    

@app.route('/game.html')
def game1():
    return send_file('templates/game.html')

@app.route('/game2.html')
def game2():
    return send_file('templates/game2.html')

@app.route('/game3.html')
def game3():
    return send_file('templates/game3.html')

@app.route('/games.html')
def games():
    return send_file('templates/games.html')

@app.route('/people.html')
def people():
    return send_file('templates/people.html')

@app.route('/person.html')
def person1():
    return send_file('templates/person.html')

@app.route('/person2.html')
def person2():
    return send_file('templates/person2.html')

@app.route('/person3.html')
def person3():
    return send_file('templates/person3.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
