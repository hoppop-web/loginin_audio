from flask import Flask, request, redirect, url_for, render_template
import subprocess
import os

app = Flask(__name__)
allowed_uids = ['11011', '22022', '33033']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_filename = 'static/audio/input.flac'
        uid = request.form['uid']
        output_filename = "{}_{}.flac".format(os.path.splitext(input_filename)[0], uid)
        if uid in allowed_uids:
            if os.path.exists(output_filename):
                return redirect(url_for('download', filename=output_filename, uid=uid))
            else:
                subprocess.run(
                    ['ffmpeg', '-i', input_filename, '-metadata', 'user='+uid, output_filename])
                return redirect(url_for('download', filename=output_filename, uid=uid))
        else:
            return 'Error: 权限不够'
    return render_template('index.html')


@app.route('/download/<uid>')
def download(uid):
    output_filename = "audio/input_{}.flac".format(uid)
    return render_template('download.html', uid=uid, output_filename=output_filename)


if __name__ == '__main__':
    app.run()


