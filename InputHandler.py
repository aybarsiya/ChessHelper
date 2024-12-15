"""
        InputHandler Module

        This module is responsible for real time keyboard and mouse I/O.

        Aybars Ay
        2024
"""

from pynput import keyboard
from pynput import mouse
from google.cloud import speech

from Enums import MS_PER_FRAME
from threading import Thread, Lock
from time import sleep

class _InputHandler():

        listening = True
        update = False

        def Start(self):
                self._listener = keyboard.Listener(on_press = self._KeyboardPress, on_release = self._KeyboardRelease)
                self._listener.start()
                Thread(target = self.Loop).start()

        def Loop(self):
                while(self.listening):
                        sleep(0.16)
                        print("on")


        def Stop(self):
                self._listener.stop()

        @staticmethod
        def _KeyboardPress(key: keyboard.KeyCode):

                print(key)

        def _KeyboardRelease(self, key: keyboard.KeyCode):
                print('{0} released'.format(key))
                if key == keyboard.Key.esc:
                        # Stop listener
                        self.listening = False
                        self._listener.stop()
                        return False
                elif key == keyboard.Key.enter:
                        self.update = True


        pass

IH = _InputHandler()

class speechToText():

        def run_quickstart(self):
                # Instantiates a client
                client = speech.SpeechClient()

                # The name of the audio file to transcribe
                gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

                audio = speech.RecognitionAudio(uri=gcs_uri)

                config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code="en-US",)

                # Detects speech in the audio file
                response = client.recognize(config=config, audio=audio)

                for result in response.results:
                        print(f"Transcript: {result.alternatives[0].transcript}")

        def test():
                client = speech.AdaptationAsyncClient()

        pass

# """PyAudio Example: Play a wave file (callback version)."""

# import wave
# import time
# import sys

# import pyaudio


# if len(sys.argv) < 2:
#     print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#     sys.exit(-1)

# with wave.open(sys.argv[1], 'rb') as wf:
#         # Define callback for playback (1)
#         def callback(in_data, frame_count, time_info, status):
#                 data = wf.readframes(frame_count)
#                 # If len(data) is less than requested frame_count, PyAudio automatically
#                 # assumes the stream is finished, and the stream stops.
#                 return (data, pyaudio.paContinue)

#         # Instantiate PyAudio and initialize PortAudio system resources (2)
#         p = pyaudio.PyAudio()

#         # Open stream using callback (3)
#         stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                         channels=wf.getnchannels(),
#                         rate=wf.getframerate(),
#                         output=True,
#                         stream_callback=callback)

#         # Wait for stream to finish (4)
#         while stream.is_active():
#                 time.sleep(0.1)

#         # Close the stream (5)
#         stream.close()

#         # Release PortAudio system resources (6)
#         p.terminate()

# https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
# https://pypi.org/project/pynput/
# https://raspberrypi.stackexchange.com/questions/55431/read-keyboad-input-from-background-process
# https://docs.python.org/3/library/threading.html
# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing
# https://cloud.google.com/python/docs/reference/speech/latest
# https://cloud.google.com/speech-to-text/docs/samples/speech-streaming-recognize?hl=en
# https://cloud.google.com/python/docs/reference/speech/latest/google.cloud.speech_v1.services.speech.SpeechClient#google_cloud_speech_v1_services_speech_SpeechClient_long_running_recognize
# https://googleapis.dev/python/google-api-core/latest/client_options.html
# https://cloud.google.com/speech-to-text/docs/transcribe-client-libraries

# https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.Stream.__init__
# https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.Stream