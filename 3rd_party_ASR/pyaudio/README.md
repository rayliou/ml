
# OpenAI SDK
- https://platform.openai.com/docs/api-reference/introduction

# Deepgram SDK
- https://github.com/deepgram/deepgram-python-sdk
- https://developers.deepgram.com/docs/python-sdk-streaming-transcription
# API key:
- d263b67a41437cb1a1ddb2bef57efa3fc1d360a5

# FYI

- https://github.com/DamienDeepgram/satori
- https://github.com/deepgram/streaming-test-suite
- https://developers.deepgram.com/reference/streaming#stream-keepalive
- https://developers.deepgram.com/docs/encoding
- https://developers.deepgram.com/docs/sample-rate
- https://developers.deepgram.com/docs/endpointing




```mermaid
sequenceDiagram
    participant ED as Embedded Device
    participant AS as ASR Server
    participant LLM as LLM Server

    ED->>ED: Detects "Go to Cloud" command
    ED->>AS: Initializes and Establishes websocket connection
    ED->>LLM: Initializes and Establishes Restful connection

    Note over ED,AS: Real-time interaction begins
    ED->>AS: Sends Live Stream Audio
    AS-->>ED: Returns text data real-time
    ED->>ED: Checks for timeout or multiple silence instances

    alt Continuous Audio Stream
        AS-->>ED: Returns text data real-time
    else Timeout or Multiple Silence Instances
        AS-->>ED: Disconnects after 12 sec timeout or multiple silence instances
        ED->>ED: Concatenates all received text data
        ED->>LLM: Sends the concatenated text as question
        LLM-->>ED: Sends back answer
        ED->>ED: Prints the answer on the console
    end

```

