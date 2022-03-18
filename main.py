from flask import Flask, render_template, redirect, url_for, request, redirect
from flask_bootstrap import Bootstrap
from spotify_api import episodes, search_episodes
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporarysecretkey'  # replace this with enviroment variable on deployment


class SearchForm(FlaskForm):
    search_entry = StringField('search', validators=[DataRequired()])
    submit = SubmitField("Search")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', episodes=episodes)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST' and request.form["search_entry"]:
        search_results = search_episodes(request.form["search_entry"])
        print(request.form["search_entry"])
        print(search_results)
        if search_results:
            return render_template('search.html', search_results=search_results)
    return redirect(url_for('home'))


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
