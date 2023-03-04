import azure.cognitiveservices.speech as speechsdk

class TTS:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription='TOKEN HERE', endpoint="https://centralus.api.cognitive.microsoft.com/sts/v1.0/issuetoken")
        self.audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
        
        self.speech_config.speech_synthesis_language = "en-US"
        self.speech_config.speech_synthesis_voice_name ="en-US-JennyNeural"

    def speak(self, text):
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

    
        
        

    