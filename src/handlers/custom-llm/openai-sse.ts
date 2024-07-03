import { Request, Response } from 'express';
import fetch from 'node-fetch';
import { PassThrough } from 'stream';


async function voiceflowToOpenAIStream(voiceflowResponse, onChunk) {
  let content = '';
  console.log('Voiceflow response status:', voiceflowResponse.status);
  console.log('Voiceflow response headers:', voiceflowResponse.headers);

  const reader = voiceflowResponse.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    console.log('Raw chunk:', chunk);

    const lines = chunk.split('\n');
    for (const line of lines) {
      if (line.trim() === '') continue;

      console.log('Processing line:', line);

      if (line.startsWith('data:')) {
        const jsonData = line.slice(5).trim();
        try {
          const data = JSON.parse(jsonData);
          if (data.type === 'trace' && data.trace.type === 'completion-continue') {
            content += data.trace.payload.completion;
            onChunk({
              choices: [{
                delta: { content: data.trace.payload.completion },
                index: 0,
                finish_reason: null
              }]
            });
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      }
    }
  }

  console.log('Final content:', content);

  onChunk({
    choices: [{
      delta: {},
      index: 0,
      finish_reason: 'stop'
    }]
  });
}

export const openaiSSE = async (req: Request, res: Response) => {
  try {
    const {
      model,
      messages,
      max_tokens,
      temperature,
      call,
      stream,
      ...restParams
    } = req.body;

    // delete restParams.metadata;

    console.log(req.body);
    const voiceflowUrl = 'https://general-runtime.voiceflow.com/v2beta1/interact/66854b1150071d75d0bdd702/development/stream';
    const voiceflowHeaders = {
      'Accept': 'text/event-stream',
      'Authorization': 'VF.DM.66854b63a012b6c03983587f.2guwZJauMOEnwceM',
      'Content-Type': 'application/json'
    };
    console.log('Message:', req.body.messages[req.body.messages.length - 1].content);
    const voiceflowBody = {
      action: {
        type: 'intent',
        payload: {
          intent: { name: 'receive_message' },
          query: req.body.messages[req.body.messages.length - 1].content
        }
      },
      session: {
        userID: '1234',
        sessionID: 'session_123'
      }
    };

    try {
      const voiceflowResponse = await fetch(voiceflowUrl, {
        method: 'POST',
        headers: voiceflowHeaders,
        body: JSON.stringify(voiceflowBody)
      });

      if (!voiceflowResponse.ok) {
        throw new Error(`Voiceflow API responded with status ${voiceflowResponse.status}`);
      }

      // console.log('Voiceflow Response:', voiceflowResponse);

      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      });

      const stream = new PassThrough();
      stream.pipe(res);

      await voiceflowToOpenAIStream(voiceflowResponse, (chunk) => {
        console.log('Chunk:', chunk);
        stream.write(`data: ${chunk}\n\n`);
      });

      stream.end();

    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'An error occurred while processing your request.' });
    }
  } catch (e) {
    console.log('Error:', e);
    res.status(500).json({ error: e });
  }
};
