from .db import db


class Mars(db.Document):

    news_title = db.StringField(required=True)
    news_p = db.StringField(required=True)
    featured_image = db.StringField(required=True)
    current_weather = db.StringField(required=True)
    table_html = db.StringField(required=True)
    hemi_full_image_urls = db.ListField(required=True)

    meta = {'alias': 'core', 'collection': 'mars'}
