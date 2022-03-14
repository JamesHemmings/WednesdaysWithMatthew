from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from spotify_api import episodes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporarysecretkey'  # replace this with enviroment variable on deployment
print(episodes[0])

@app.route('/')
def home():
    return render_template('index.html', episodes=episodes)


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
