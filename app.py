from flask import Flask, render_template, abort, send_from_directory
import markdown
from pathlib import Path
import os
from datetime import datetime

app = Flask(__name__)

#testing123

@app.route('/')
def index():
    posts = []
    postsDir = Path('posts')
    for file in postsDir.glob('*.md'):
        title = file.stem
        creationTime = os.path.getctime(file)
        creationDate = datetime.fromtimestamp(creationTime).strftime('%Y-%m-%d')
        posts.append({
            'id': title,
            'title': title,
            'date': creationDate,
            'timestamp': creationTime  # Add timestamp for sorting
        })
    
    
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    blurb = ''
    try:
        with open('posts/blurb.txt', 'r') as f:
            blurb = f.read().strip()
    except FileNotFoundError:
        blurb = "Welcome to my blog!"

    
    return render_template('index.html', posts=posts, blurb=blurb)

@app.route('/post/<postId>')
def showPost(postId):
    postPath = Path('posts') / f'{postId}.md'
    
    if not postPath.exists():
        abort(404)
    creationTime = os.path.getctime(postPath)
    creationDate = datetime.fromtimestamp(creationTime).strftime('%Y-%m-%d')

    with open(postPath) as f:
        content = markdown.markdown(f.read())
        post = {'id': postId, 'content': content, 'title': postId, 'date': creationDate}
    
    return render_template('post.html', post=post)

@app.route('/images/<path:filename>')
def serveImages(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)