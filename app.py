from flask import Flask,render_template,request
from urllib import parse as urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import json
from summarizer import Summarizer,TransformerSummarizer

app = Flask(__name__)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        vid_link = form_data["Video Link"]
        vid = video_id(vid_link)
        summ = yt_summarizer(vid)
        vid_data = {"Video Link": summ}
        return render_template('data.html',form_data = vid_data)


def video_id(value):
    query = urlparse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def yt_summarizer(vid):
    subs = YouTubeTranscriptApi.get_transcript(vid)
    outfile = open('output.txt', 'w')
    sub_list1 = []
    subs_list2 = []
    for i in range(len(subs)):
        sub_list1.append(subs[i]['text'])

    for x in sub_list1:
        subs_list2.append(x.replace("\n", " "))

    final_subtitles = ""

    for y in subs_list2:
        final_subtitles += y + " "

    text = final_subtitles
    outfile.write(final_subtitles)

    bert_model = Summarizer()
    bert_summary = ''.join(bert_model(text, min_length=60))
    return bert_summary

app.run(host='localhost', port=5000)