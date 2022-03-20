from flask import Flask, render_template, redirect, url_for, request, redirect
from flask_bootstrap import Bootstrap
from spotify_api import episodes, search_episodes
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email,ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporarysecretkey'  # replace this with enviroment variable on deployment


def is_female(form, field):
    if not field.data:
        raise ValidationError('Sorry must be female to message me')


class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired(message="is that really your name?")])
    email = EmailField(validators=[Email(message="that's not your email try harder pal!")])
    message = TextAreaField(validators=[DataRequired(message="you need to fill this out nincompoop")])
    female = BooleanField(validators=[is_female])
    submit = SubmitField()


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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        print("form validate")
    message_sent = True
    return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
