# Web Scraping Homework - Mission to Mars

## Instruction

### MongoDB set up

Replace MongoDB host to your own.

```python
# in app.py
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB'),
}
```

### Run Flask application

```sh
$ export FLASK_APP=src/app.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

### Jupyter Notebook NB View link

https://nbviewer.jupyter.org/github/moz5691/web-scraping-challenge/blob/master/mission_to_mars.ipynb

### Screenshot of the application

![mission_to_mars](img/screen_shot.png)
