import re
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def index():
    return open('/Users/narimatsuhinata/Desktop/youtube_transcriber/index.html').read()

def get_id(url):
    m = re.search(r'(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})', url)
    return m.group(1) if m else None

@app.route('/transcribe', methods=['POST'])
def transcribe():
    url = request.json.get('url', '')
    vid = get_id(url)
    if not vid:
        return jsonify({'error': '有効なYouTube URLではありません'})
    try:
        ytt = YouTubeTranscriptApi()
        data = ytt.fetch(vid, languages=['ja', 'en'])
    except Exception as e:
        return jsonify({'error': str(e)})
    lines = []
    for e in data:
        s = int(e.start)
        m, s2 = divmod(s, 60)
        h, m = divmod(m, 60)
        t = f'[{h:02d}:{m:02d}:{s2:02d}]' if h else f'[{m:02d}:{s2:02d}]'
        lines.append(f'{t} {e.text.strip()}')
    return jsonify({'text': '\n'.join(lines), 'count': len(lines)})

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://localhost:5000')
    app.run(debug=False)

