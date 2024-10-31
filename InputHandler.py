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
import multiprocessing as mp; from multiprocessing import Process
from time import sleep

class _InputHandler():

        running = True

        def Start(self):
                self._listener = keyboard.Listener(on_press = self._KeyboardPress, on_release = self._KeyboardRelease)
                self._listener.start()

        def Stop(self):
                self._listener.stop()

        @staticmethod
        def _KeyboardPress(key: keyboard.KeyCode):

                print(key)

        def _KeyboardRelease(self, key: keyboard.KeyCode):
                print('{0} released'.format(key))
                if key == keyboard.Key.esc:
                        # Stop listener
                        self.running = False
                        return False


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

# https://pypi.org/project/pynput/
# https://raspberrypi.stackexchange.com/questions/55431/read-keyboad-input-from-background-process
# https://docs.python.org/3/library/threading.html
# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing
# https://cloud.google.com/python/docs/reference/speech/latest
# https://cloud.google.com/speech-to-text/docs/samples/speech-streaming-recognize?hl=en
# https://cloud.google.com/python/docs/reference/speech/latest/google.cloud.speech_v1.services.speech.SpeechClient#google_cloud_speech_v1_services_speech_SpeechClient_long_running_recognize
# https://googleapis.dev/python/google-api-core/latest/client_options.html
# https://cloud.google.com/speech-to-text/docs/transcribe-client-libraries