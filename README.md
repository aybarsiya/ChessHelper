# **ChessHelper**

This is a Python program, that allows users to play chess with voice commands. This is an accessibility tool for users with limited physical interaction with the computer, translating from verbal commands to mouse and keyboard inputs, with on screen automatic chessboard detection capabilities.

## The program can:
  -	Find a chessboard on the screen (only supports Chess.com’s assets for now but can be extended, classes’ structures are designed for this)
  -	Determine the scale of the chessboard on the screen compared to assets’ original sizes.
    -	Tries to find a chessboard piece on the screen, if it does not find one, means that there is no chessboard on the screen.
  -	Initialize Chessboard object
    -	Contains cropped images of squares of the chessboard for each square, ultimately the pieces are determined by image processing functions from ScreenHandler class.
  -	Record voice from the microphone
    -	After the recording is finished, Google Cloud’s speech to text API is used to get the text form of the microphone input
    -	(Recording is done manually (records while a key is being held down) for now to keep gCloud costs low, in newer iterations of this program, “play” keyword can be utilized to determine when a user wants to make a move)
  -	Make chess moves on the screen with the speech-to-text input
    -	Determines the source and the destination squares from the input
    -	Tries to make a move by simulating mouse movements and clicks
    -	If a move was not successfully made, it informs the user of this outcome
    -	Same colour piece to same colour piece squares cannot be in the same input
    -	If a move was successful, the program captures another screenshot to update the Chessboard object and recalculates pieces on the squares (This can be improved by just requesting to update the changed squares)
## Inputs:
  -	Keyboard
    -	Right control key: initializes the chessboard by taking the initial screenshot of the screen, finds the chessboard and determines pieces for every square
    -	(Holding) Scroll lock key: Turns on the microphone and starts recording immediately until the key is released. After the recording, ChessHelper object sees that there is a recording, forwards it to _Speech object to send a request to Google Cloud Speech-to-Text API, gets the result in string, then uses this string to try to make a move.
    -	Esc key: Exits the whole program

## Third-Party Libraries Used:
  - OpenCV
  - Pillow
  - numpy
  - pynput
  - pyaudio
  - google.cloud.speech
  - playsound
