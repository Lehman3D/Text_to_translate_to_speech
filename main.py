import json
from ibm_watson import LanguageTranslatorV3
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import simpleaudio as sa


def main():
    translator_apikey = "enter_api_key"
    text_to_speech_apikey = "enter_api_key"
    translator_url = "enter_url"
    text_to_speech_url = "enter_url"
    version = "2018-05-01"

    # authenticate the translator and the text to speech
    authenticator = IAMAuthenticator(translator_apikey)
    language_translator = LanguageTranslatorV3(
        version=version,
        authenticator=authenticator
    )
    authenticator2 = IAMAuthenticator(text_to_speech_apikey)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator2
    )

    # identify the Endpoint URLs
    language_translator.set_service_url(translator_url)
    text_to_speech.set_service_url(text_to_speech_url)

    languages = {'arabic': 'en-ar', 'chinese': 'en-zh', 'french': 'en-fr', 'german': 'en-de', 'japanese': 'en-ja',
                 'korean': 'en-ko', 'spanish': 'en-es'}

    voices = {'arabic': 'ar-MS_OmarVoice', 'chinese': 'zh-CN_LiNaVoice', 'french': 'fr-FR_ReneeV3Voice',
              'german': 'de-DE_DieterV3Voice', 'japanese': 'ja-JP_EmiV3Voice', 'korean': 'ko-KR_YoungmiVoice',
              'spanish': 'es-LA_SofiaV3Voice'}

    # get the language
    print("Please enter the langauge you want translated:\nOptions: ", end="")
    for lang in languages:
        print(lang + ", ", end="")
    print("")

    # get input from user
    lang = input()

    # check if input not in dictionary and exit
    if lang not in languages:
        print("Language input invalid. Goodbye")
        exit(1)

    # get the language model and voice from the dictionaries
    lang_model = languages[lang]
    voice = voices[lang]

    filename = 'hello_world.wav'

    # loop asking the user for input
    while True:
        print("Please enter the text you want to translate, or type exit:")
        text = input()

        if text == 'exit':
            exit(1)

        # translate the text
        translation = language_translator.translate(
            text=text,
            model_id=lang_model).get_result()

        translation_speech = translation['translations'][0]['translation']
        print(translation_speech)

        # create the audio file
        with open(filename, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    text=translation_speech,
                    voice=voice,
                    accept='audio/wav'
                ).get_result().content)

        # read the audio file
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
