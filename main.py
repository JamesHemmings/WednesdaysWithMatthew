from flask import Flask, render_template, redirect, url_for, request, redirect
from flask_bootstrap import Bootstrap
from spotify_api import episodes, search_episodes
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
import smtplib
import os
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
year = datetime.today().year


@app.context_processor
def inject_year():
    return dict(year=year)




def is_female(form, field):
    if not field.data:
        raise ValidationError('Sorry must be female to message me')


class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired(message="is that really your name?")])
    email = EmailField(validators=[Email(message="that's not your email try harder pal!")])
    message = TextAreaField(validators=[DataRequired(message="you need to fill this out nincompoop")])
    submit = SubmitField()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', episodes=episodes)


@app.route('/episodes')
def all_episodes():
    return render_template('episodes.html', episodes=episodes)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST' and request.form["search_entry"]:
        search_results = search_episodes(search_term=request.form["search_entry"], episode_list=episodes)
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
        try:
            response = requests.post(
                "https://api.mailgun.net/v3/www.wednesdays-with-matthew.com/messages",
                auth=("api", MAILGUN_API_KEY),
                data={"from": "Poop <Contact@wednesdays-with-matthew.com>",
                      "to": ["james.richard.hemmings@gmail.com"],
                      "subject": f"contact form message from {form.name.data}",
                      "text": f"{form.message.data}\nemail: {form.email.data}"})

            response.raise_for_status()
            return render_template('contact.html', form=form, email_sent=True)
        except requests.exceptions.HTTPError:
            return "Sorry this isn't working correctly right now :( probably because I don't want to pay for mailgun api"

    return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
