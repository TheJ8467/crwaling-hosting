from main import fetch_articles, fetch_sub_articles
from io import BytesIO
from urllib.parse import unquote
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, send_file
import os
import psycopg2
import dotenv

dotenv.load_dotenv()

conn = psycopg2.connect(os.environ['DATABASE_URL'])
app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AnsanNewsReact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_src = db.Column(db.String, nullable=True, default=None)
    link = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/image-proxy', methods=['GET'])
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return 'No URL provided', 400

    decoded_image_url = unquote(image_url)
    response = requests.get(decoded_image_url)
    if response.status_code != 200:
        return f'Error fetching image: {response.status_code}', response.status_code

    return send_file(BytesIO(response.content), mimetype=response.headers['content-type'])


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all", methods=['GET'])
def all_news():
    all_news = db.session.query(AnsanNewsReact).all()
    news_dict = {"news": []}

    for news in all_news:
        news_data = {
            'img_src': news.img_src,
            'link': news.link,
            'title': news.title,
            'desc': news.desc
        }
        news_dict["news"].append(news_data)

    return jsonify(news_dict)

def save_articles(articles):
    db.session.query(AnsanNewsReact).delete()
    db.session.commit()

    for article in articles:
        try:
            news = AnsanNewsReact(
                img_src=article['img_src'],
                link=article['link'],
                title=article['title'],
                desc=article['desc']
            )
        except KeyError:
            news = AnsanNewsReact(
                link=article['link'],
                title=article['title'],
                desc=article['desc']
            )
            db.session.add(news)
        else:
            db.session.add(news)

    db.session.commit()


with app.app_context():
    articles = fetch_articles() + fetch_sub_articles()
    save_articles(articles)

if __name__ == '__main__':
    app.run(debug=True)