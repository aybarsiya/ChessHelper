"""
        InputHandler Module

        This module is responsible for real time keyboard, speech and mouse I/O.

        Aybars Ay
        2024
"""

from pynput import keyboard
from pynput import mouse

import pyaudio
import wave
from google.cloud import speech

from Enums import MS_PER_FRAME
from threading import Thread, Lock
from time import sleep

class _Speech():
        """
                This class is responsible of requesting and receiving of speech to text operations.
        """
        latestResponseText = ""
        responseTextAvailable = False

        def GetAudioResponse(self, audioData: bytes) -> speech.RecognizeResponse:
                """
                        Returns a string which contains what was said in the microphone recording, by getting a response from google cloud speech api.
                """
                client = speech.SpeechClient()

                audio = speech.RecognitionAudio(content=audioData)
                config = speech.RecognitionConfig(
                                                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                                sample_rate_hertz=16000,
                                                language_code="en-US",
                                                )

                response = client.recognize(config=config, audio=audio)
                print ("speech to text request sent")

                responseText = ""
                for result in response.results:
                        # The first alternative is the most likely one for this portion.
                        responseText += result.alternatives[0].transcript

                self.latestResponseText = responseText.replace(" ", "")
                self.responseTextAvailable = True
                print ("speech to text response received")

                print(self.latestResponseText)

        def GetResponse(self):
                self.responseTextAvailable = False
                return self.latestResponseText

class _Microphone():
        """
                This class is responsible for recording audio from the default microphone on the device.
        """
        listening = False
        latestData: bytes
        dataAvailable = False

        _sample_format = pyaudio.paInt16
        _channels = 1
        _rate = 16000
        _chunk: int

        def __init__(self):
                self._chunk = int(self._rate / 20)

        def Listen(self):
                self.listening = True
                p = pyaudio.PyAudio()

                stream = p.open(format=self._sample_format,
                                        channels=self._channels,
                                        rate=self._rate,
                                        frames_per_buffer=self._chunk,
                                        input=True)

                frames = []

                print ("microphone on")
                while self.listening:

                        data = stream.read(self._chunk)
                        frames.append(data)
                        sleep(1 / 800)

                for i in range(2):
                        data = stream.read(self._chunk)
                        frames.append(data)
                        sleep(1 / 800)
                print ("microphone off")

                stream.stop_stream()
                stream.close()
                p.terminate()

                self.latestData = b''.join(frames)
                self.dataAvailable = True

        def GetData(self):
                self.dataAvailable = False
                return self.latestData

        pass

class _Mouse():
        """
                This class makes moves on screen.
        """
        def MakeMove(self, pos1: tuple[int, int], pos2: tuple[int, int]):

                print ("making move")
                print(pos1, pos2)
                mouseController = mouse.Controller()

                sleep(MS_PER_FRAME / 1000)

                mouseController.position = pos1
                sleep(MS_PER_FRAME / 1000)

                mouseController.press(mouse.Button.left)

                sleep(MS_PER_FRAME / 1000)

                mouseController.position = pos2

                sleep(MS_PER_FRAME / 1000)

                mouseController.release(mouse.Button.left)

                sleep(MS_PER_FRAME / 1000)

                mouseController.position = (480, 1079)
                print ("finished making move")

        pass

class _Keyboard():
        """
                This class is responsible for handling the whole program by getting threaded inputs from the keyboard.
        """
        _listening = True
        _microphoneOn = False
        _initializeChessBoard = False

        def Start(self):
                self._listener = keyboard.Listener(on_press = self._KeyboardPress, on_release = self._KeyboardRelease)
                self._listener.start()

                print("keyboard on")


        def Stop(self):
                self._listener.stop()
                self._listening = False


        def _KeyboardPress(self, key: keyboard.KeyCode):

                if ((not self._microphoneOn) and key == keyboard.Key.scroll_lock):
                        self._microphoneOn = True

                elif ((not self._initializeChessBoard) and key == keyboard.Key.ctrl_r):
                        self._initializeChessBoard = True


        def _KeyboardRelease(self, key: keyboard.KeyCode):
                print('{0} released'.format(key))
                if (key == keyboard.Key.esc):
                        self.Stop()

                elif (key == keyboard.Key.scroll_lock):
                        self._microphoneOn = False


        pass

class _InputHandler():
        """
                This class is the main handler of all I/O classes.
        """
        _keyboard: _Keyboard
        _mouse: _Mouse
        _microphone: _Microphone
        _speech: _Speech

        def __init__(self):


                self._keyboard = _Keyboard()
                self._mouse = _Mouse()
                self._microphone = _Microphone()
                self._speech = _Speech()

                self._keyboard.Start()

                Thread(target = self.Loop).start()

        def Loop(self):
                while(self._keyboard._listening):
                        sleep(MS_PER_FRAME / 1000)

                        if ((not self._microphone.listening) and (not self._microphone.dataAvailable) and self._keyboard._microphoneOn):
                                Thread(target = self._microphone.Listen).start()

                        if ((not self._keyboard._microphoneOn) and self._microphone.listening):
                                self._microphone.listening = False

                        if(self._microphone.dataAvailable):
                                microphoneData = self._microphone.GetData()
                                Thread(target = self._speech.GetAudioResponse, args = [microphoneData, ]).start()

IH = _InputHandler()

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