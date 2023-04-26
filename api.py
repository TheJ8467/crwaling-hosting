from flask import Flask, jsonify, render_template
import os
import psycopg2
import dotenv
from models import db, AnsanNewsReact

dotenv.load_dotenv()

conn = psycopg2.connect(os.environ['DATABASE_URL'])
app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def load_articles_from_database():
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

    return news_dict

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/all', methods=['GET'])
def all_news():
    articles = load_articles_from_database()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
