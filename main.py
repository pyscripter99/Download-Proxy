from flask import Flask, send_file, request, render_template
from io import BytesIO
import urllib.parse
import requests

app = Flask(__name__)

def get_filename_from_url(url):
    
    parsed_url = urllib.parse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    if len(filename)>0:

        # Remove trailing slash
        if filename[-1:]=="/":
            filename = filename[:-1]
        
        if "/" in filename:
            filename = filename.split("/")[-1]

    return filename 

@app.route("/")
def home():
    return render_template("download.html")

@app.route("/download/")
def download():
    r = requests.get(request.args.get("url"))
    b = BytesIO(r.content)
    b.name = get_filename_from_url(request.args.get("url"))
    return send_file(b, mimetype=r.headers['Content-Type'].split(";")[0], as_attachment=True, download_name=get_filename_from_url(request.args.get("url")))

app.run("0.0.0.0", 80)