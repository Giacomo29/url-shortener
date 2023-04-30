from  flask import Flask, render_template, request, redirect, url_for 

import random
import string
import json

app = Flask(__name__)
shortened_urls = {}


def generate_short_url(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_url = generate_short_url()

        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = url
        with open('urls.json', 'w') as urls_file:
            json.dump(shortened_urls, urls_file)
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template('index.html')



@app.route('/<short_url>')
def redirect_to_url(short_url):
    if short_url in shortened_urls:
        return redirect(shortened_urls[short_url])
    return f"URL for '{short_url}' doesn't exist", 404



if __name__ == '__main__':
    try:
        with open('urls.json', 'r') as urls_file:
            shortened_urls = json.load(urls_file)
    except Exception as e:
        print(e)
    app.run(debug=True)