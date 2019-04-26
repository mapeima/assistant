import speech_recognition as sr
from tempfile import TemporaryFile
from gtts import gTTS
from pygame import mixer
from googletrans import Translator
import webbrowser


lang = 'es-es'
av_lang = {'english': 'en-us', 'spanish': 'es-es', 'german': 'de-de'}
act_phrase = {'en-us': 'Hi Python', 'es-es': 'Hola Python', 'de-de': 'Hallo Python'}

av_sites = {'youtube': 'https://www.youtube.com/results?search_query=', 'amazon': 'https://www.amazon.es/s?k=',
            'ebay': 'https://www.ebay.com/sch/i.html?_nkw=', 'wikipedia': 'https://es.wikipedia.org/wiki/'}


r = sr.Recognizer()
mic = sr.Microphone()
tr = Translator()


def listen():
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio, language=lang)
            le_text = str(tr.translate(text).text).lower()
            print('---' + le_text)
            return text, le_text

    except sr.UnknownValueError:
        print("+++No te he entendido :(")

        raise sr.UnknownValueError

    except Exception as e:
        raise e


def say(text):
    lg = lang.split('-')[0]
    tr_text = tr.translate(text, lg).text
    print('+++' + tr_text)
    tts = gTTS(tr_text, lg)
    tf = TemporaryFile()
    tts.write_to_fp(tf)
    tf.seek(0)

    while mixer.music.get_busy():
        pass

    mixer.music.load(tf)
    mixer.music.play()


def activate():
    try:
        text, _ = listen()

    except sr.UnknownValueError:
        return False

    if text and text.lower() == act_phrase[lang].lower():
        return True

    else:
        return False


def main():
    global lang

    mixer.init()

    while not activate():
        pass

    while True:

        say('¿En qué te puedo ayudar?')

        try:
            text, le_text = listen()

        except sr.UnknownValueError:
            continue

        if text != '':
            if le_text.startswith('change the language to '):
                lg = le_text.split('change the language to ')[1]

                if lg in av_lang:
                    lang = av_lang[lg]

                    say('Idioma cambiado a ' + lg)

            elif le_text.startswith('search on ') or le_text.startswith('search in ')\
                    or le_text.startswith('search wikipedia '):

                site, search = le_text.replace('search on ', '').replace('search in ', '')\
                    .replace('search ', '').split(' ', 1)
                print(1)
                if site == 'wikipedia':
                    search = '_'.join([b.capitalize() for b in search.split()])

                address = av_sites[site] + search.replace(' ', '+')

                webbrowser.open(address)

                say('Buscando en ' + site + ' ' + search)

            elif le_text.startswith('look for ') or le_text.startswith('search ') or le_text.startswith('seek'):
                search = le_text.replace('look for ', '').replace('search ', '').replace('seek ', '')
                print(2)
                address = 'https://www.google.com/search?q=' + search

                webbrowser.open(address)

                say('Buscando en google ' + search)

            if le_text == 'exit' or le_text == 'bye':
                break

            if le_text == 'wait':
                say('Hasta luego!')
                while not activate():
                    pass

                continue


if __name__ == '__main__':
    main()
