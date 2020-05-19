import os
from flask import Flask, render_template, redirect
from nosql.db import initialize_db
from nosql.mars import Mars
from utils.scrape import scrape_all
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__),
                        '..')  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB'),
}

initialize_db(app)


@app.route('/')
def index():

    mars_data = Mars.objects().order_by('-id').first()
    return render_template("index.html", mars_data=mars_data)


@app.route('/scrape')
def scrape():
    mars_data = scrape_all()
    mars = Mars()
    mars.news_title = mars_data['news_title']
    mars.news_p = mars_data['news_p']
    mars.featured_image = mars_data['featured_image']
    mars.current_weather = mars_data['current_weather']
    mars.table_html = mars_data['table_html']
    mars.hemi_full_image_urls = mars_data['hemi_full_image_urls']
    mars.save()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
