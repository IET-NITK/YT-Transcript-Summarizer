#!/home/naveen/YTS/venv/bin
from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return "hello world!"

@app.route('/<video_id>')
def get_transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    import transformers 
    import sentencepiece 
    data=YouTubeTranscriptApi.get_transcript(video_id)
    transcript=''
    for value in data:
        for key,val in value.items():
            if key=='text':
                transcript+=val
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    #T5 small
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    inputs = tokenizer.encode("summarize: "+transcript, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs, 
        max_length=150, 
        min_length=40, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True)
    output=' Text:-\n' + transcript + '\n\nSummary:-\n'
    output+=tokenizer.decode(outputs[0])
    return output

@app.errorhandler(404)
def not_found(e):
    return "404.html"

if __name__ == '__main__':
    app.run(debug=True)