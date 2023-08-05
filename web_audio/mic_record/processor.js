
var fluentai_msg  = null;

class WorkletProcessor extends AudioWorkletProcessor {
 constructor(options) {
    super(options);
    this._heapInputBuffer = new HeapAudioBuffer(
        Module, RENDER_QUANTUM_FRAMES, 2, MAX_CHANNEL_COUNT);
    this._heapOutputBuffer = new HeapAudioBuffer(
        Module, RENDER_QUANTUM_FRAMES, 2, MAX_CHANNEL_COUNT);
    this._kernel = new Module.FluentaiKernel();
  }

  process(inputs, outputs, parameters) {
    fluentai_msg  = null;
  // Use the 1st input and output only to make the example simpler. |input|
    // and |output| here have the similar structure with the AudioBuffer
    // interface. (i.e. An array of Float32Array)
    const input = inputs[0];
    const output = outputs[0];

    // For this given render quantum, the channel count of the node is fixed
    // and identical for the input and the output.
    const channelCount = input.length;

    // Prepare HeapAudioBuffer for the channel count change in the current
    // render quantum.
    this._heapInputBuffer.adaptChannel(channelCount);
    this._heapOutputBuffer.adaptChannel(channelCount);

    // Copy-in, process and copy-out.
    for (let channel = 0; channel < channelCount; ++channel) {
      this._heapInputBuffer.getChannelData(channel).set(input[channel]);
    }
    this._kernel.process(
        this._heapInputBuffer.getHeapAddress(),
        this._heapOutputBuffer.getHeapAddress(),
        channelCount);

    if (fluentai_msg) {
      //console.log("Returned the JS env:" +  fluentai_msg);
      this.port.postMessage(fluentai_msg);
    }
    for (let channel = 0; channel < channelCount; ++channel) {
      output[channel].set(this._heapOutputBuffer.getChannelData(channel));
    }

    return true;
  }

}

registerProcessor("worklet-processor", WorkletProcessor);
