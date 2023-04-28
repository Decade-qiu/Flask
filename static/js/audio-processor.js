class AudioProcessor extends AudioWorkletProcessor {
    process(inputs, outputs) {
        const inputChannel = inputs[0][0];
        this.port.postMessage(inputChannel);
        return true;
    }
}
registerProcessor('audio-processor', AudioProcessor);