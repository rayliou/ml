
// processor.js
class WorkletProcessor extends AudioWorkletProcessor {
  process(inputs, outputs, parameters) {
    // Do something with the data, e.g. convert it to WAV
    console.log(inputs[0]);
    return true;
  }
}

registerProcessor("worklet-processor", WorkletProcessor);
