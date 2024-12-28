from flask import Flask, render_template, abort
import markdown
from pathlib import Path
import os
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def index():
    posts = []
    postsDir = Path('posts')
    for file in sorted(postsDir.glob('*.md'), reverse=True):
        title = file.stem
        creationTime = os.path.getctime(file)
        creationDate = datetime.fromtimestamp(creationTime).strftime('%Y-%m-%d')
        posts.append({
            'id': title,
            'title': title,
            'date': creationDate
        })
    
    return render_template('index.html', posts=posts)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)