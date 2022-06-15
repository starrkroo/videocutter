#!/usr/bin/env python

import os
import socket
from flask import Flask, render_template, request
from customs import *

app = Flask(__name__)

@app.route('/videos')
def render_videos():
	return render_template('render_videos.html', videos = os.listdir('static/videos'))

@app.route('/', methods=['POST', 'GET'])
def index():

	if request.method == 'POST':
		video_url = request.form.get('url')
		timecode_start = prepare_second(request.form.get('timecode_start'))
		timecode_end   = prepare_second(request.form.get('timecode_end'))

		videoname = download_video(video_url)

		try:
			cut_video(videoname, timecode_start, timecode_end)
		except Exception as e:
			return render_template('index.html', output_information=e)

	return render_template('index.html', output_information='OK')

if __name__ == '__main__':
	hosting = socket.gethostname()
	print(hosting)
	# hosting = '192.168.1.60'
	app.run(host=hosting, port=5004, debug=True)