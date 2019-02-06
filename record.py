#!/usr/bin/env python3

import numpy as np
from picamera import PiCamera, Color
import picamera.array
import datetime
import time
from threading import Thread, Event
import signal
import sys
import uuid

output_dir = '/videos'
quality = 20 # quality of 1 (highest) 40 (lowest)
format = 'h264'
exposure_mode = 'auto' # default is auto. Options like 'beach', 'night', etc., exist too
annotate_text_size = 32 # default is 32
min_recording_time = 10 # minimum recording length (in seconds) for any motion

last_motion = datetime.datetime.now()

class DetectMotion(picamera.array.PiMotionAnalysis):
	def analyse(self, a):
		a = np.sqrt(
			np.square(a['x'].astype(np.float)) +
			np.square(a['y'].astype(np.float))
		).clip(0, 255).astype(np.uint8)
		# If there're more than 10 vectors with a magnitude greater
		# than 60, then say we've detected motion
		if (a > 60).sum() > 10:
			global last_motion
			last_motion = datetime.datetime.now()

def async_record(camera, session_id, clip_number, thread_control):
	timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	file_path = '%s/%s.session-%s.clip-%s.h264' % (output_dir, timestamp, session_id, clip_number)

	print('record at %s' % file_path)

	# We're constantly recording to /dev/null on port 1. So capture on port 2.
	camera.start_recording(file_path, format=format, quality=quality, splitter_port=2, motion_output=output)

	while not thread_control.wait(1):
		camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		camera.wait_recording(0.1)

	print('stop recording %s' % file_path)

	camera.stop_recording(splitter_port=2)

if __name__ == "__main__":
	is_running = True
	session_id = str(uuid.uuid4())[:8]
	clip_number = 0

	def signal_handler(sig, frame):
		global is_running
		is_running = False

	signal.signal(signal.SIGINT, signal_handler)

	with PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.annotate_text_size = annotate_text_size
		camera.annotate_background = Color('blue')
		camera.annotate_foreground = Color('yellow')
		camera.exposure_mode = exposure_mode

		with DetectMotion(camera) as output:
			camera.start_recording('/dev/null', format=format, quality=quality, motion_output=output)

			thread_control = Event()
			thread = Thread(target = async_record, args = (camera, session_id, clip_number, thread_control, ))

			while is_running:
				if (datetime.datetime.now() - last_motion).seconds > 10 and thread.is_alive():
					print('no motion. idle')
					thread_control.set()
					thread.join()
				if (datetime.datetime.now() - last_motion).seconds < 10 and not thread.is_alive():
					print('motion detected. will record')
					clip_number += 1
					thread_control = Event()
					thread = Thread(target = async_record, args = (camera, session_id, clip_number, thread_control, ))
					thread.start()
				time.sleep(0.1)

			camera.stop_recording()
			sys.exit(0)



			# while (datetime.datetime.now() - start).seconds < 30:
			# 	camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			# 	camera.wait_recording(0.2)
			# camera.stop_recording()

