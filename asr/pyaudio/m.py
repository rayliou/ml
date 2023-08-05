#!/home/xiaorui/anaconda3/bin/python3
# Example filename: deepgram_test.py

from deepgram import Deepgram
import asyncio
import sys,time
import logging

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'd263b67a41437cb1a1ddb2bef57efa3fc1d360a5'

async def main():
  logger = logging.getLogger('main')
  log_level = getattr(logging, "DEBUG")
  logger.setLevel(log_level)
  handler = logging.StreamHandler()
  handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
  logger.addHandler(handler)
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Create a websocket connection to Deepgram
  # In this example, punctuation is turned on, interim results are turned off, and language is set to UK English.
  try:
    deepgramLive = await deepgram.transcription.live({
      'smart_format': True,
      'interim_results': False,
      'language': 'en-US',
      'model': 'nova',
    })
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

  # Listen for the connection to close
  deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
  start_time  = time.time()
  def handle_transcript(transcript):
      text = transcript["channel"]["alternatives"][0]["transcript"]
      #print(f"[{time.time()-start_time:.4f}]: {text}")
      logger.info(text)

  # Listen for any transcripts received from Deepgram and write them to the console
  deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, handle_transcript)

  # Listen for the connection to open and send streaming audio from the stdin to Deepgram
  cnt = 0
  while True:
    data = sys.stdin.buffer.read(4000) # 4000 250ms
    if data:
      deepgramLive.send(data)
      logger.debug(f"send data {cnt}")
      cnt += 1
    else:
      break  # break if there is no more data

  # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
  await deepgramLive.finish()

# If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
# await main()
asyncio.run(main())
