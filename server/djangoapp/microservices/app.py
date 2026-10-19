from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=16384
analyzer=SentimentIntensityAnalyzer()
def analyze(text):
    if not isinstance(text,str) or not text.strip() or len(text)>2000:
        return jsonify(error='Text must contain 1–2000 characters'),400
    scores=analyzer.polarity_scores(text)
    sentiment='positive' if scores['compound']>=0.05 else 'negative' if scores['compound']<=-0.05 else 'neutral'
    return jsonify(sentiment=sentiment,score=scores['compound'])
@app.get('/analyze/<path:text>')
def analyze_get(text):
    return analyze(text)
@app.post('/analyze')
def analyze_post():
    data=request.get_json(silent=True)
    return analyze(data.get('text') if isinstance(data,dict) else None)
@app.get('/health')
def health():
    return jsonify(status='ok')
if __name__=='__main__':
    from waitress import serve
    import os
    serve(app,host='127.0.0.1',port=int(os.getenv('PORT','5050')))
