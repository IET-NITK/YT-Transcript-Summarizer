from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import json
from summarizer import Summarizer,TransformerSummarizer

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

    bert_model = Summarizer()
    bert_summary = ''.join(bert_model(text, min_length=60))
    outfile.write(bert_summary)