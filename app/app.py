from flask import Flask, redirect, render_template, request
import requests
from urllib.parse import urljoin

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def Home():
    return render_template('home.html')

@app.route("/register", methods=["POST"])
def Register():
    url = request.form.get('URL')
    if url:
        params = {
            "orignal_url": url
        }
        response = requests.post('#apigateway endpoint to create', json=params, headers={'Accept': 'application/json'})
        if response.ok:
            data = response.json()
            if data.get('Id'):
                short_url = urljoin(request.url_root, data.get('Id').get('S'))
                return render_template('home.html', short_url=short_url)
    return render_template('home.html', message="Short URL cannot be created.")

@app.route("/<Id>", methods=["GET"])
def Redirect(Id):
    if not Id:
        return redirect('/home')
    params = {
        'Id': Id
    }
    response = requests.post('#apigateway endpoint to fetch entry', json=params, headers={'Accept': 'application/json'})
    if response.ok:
        data = response.json()
        if data.get('statusCode') == 200:
            return redirect(data.get('redirect_url'))
    return render_template('404.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/", methods=["GET"])
def Redirect_Home():
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True)