from flask import Flask, render_template, request, redirect, flash
from duckduckgo_search import DDGS
import podsearch
import yfinance  as yf
app = Flask(__name__)
app.secret_key = "WhoOwnSearchResults" #change in production

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
       search_term = request.form.get("search_term")
       if search_term[:3] == "ai|":
           resultsCHAT = DDGS().chat(str(search_term[3:]), model='claude-3-haiku')
           return render_template("ai.html",resultsCHAT=resultsCHAT,search_term=search_term)
       if search_term[:5] == "news|":
           resultsnews = DDGS().news(str(search_term[5:]), max_results=15)
           return render_template("news.html",resultsnews=resultsnews,search_term=search_term)
       if search_term[:6] == "image|":
           resultsimages = DDGS().images(str(search_term[6:]), max_results=200)
           return render_template("images.html",resultsimages=resultsimages,search_term=search_term)
       if search_term[:6] == "video|":
           resultsvid = DDGS().videos(str(search_term[6:]), max_results=10)
           return render_template("video.html",resultsvid=resultsvid,search_term=search_term)
       if search_term[:8] == "podcast|":
           resultspod = podsearch.search(str(search_term[8:]), country="IE", limit=20)
           return render_template("podcasts.html",resultspod=resultspod,search_term=search_term)
       return redirect("/"+search_term)
    return render_template("index.html")

@app.route('/<search_term>')
def search(search_term):
    results = DDGS().text(str(search_term), region='wt-wt', max_results=25)
    sr = search_term
    return render_template("results.html", results=results, sr=sr)
    
@app.route('/stock/<stock>')
def stock(stock):
    df = yf.Ticker(str(stock))
    pricecheck = df.info['regularMarketPrice']
    return render_template("stock.html", pricecheck=pricecheck)

@app.errorhandler(404)
def page_not_found(e):
    return "fudge", 404

@app.errorhandler(500)
def server_error(e):
    flash(e, category='danger')
    return render_template("index.html"), 500

