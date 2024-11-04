from datetime import datetime, timedelta

from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer(lang='ru')

bad_words = ['негр', 'дурак', 'клоун', 'блять', 'хуй', 'писька', 'убить', 'еврей', 'сука', 'блядина', 'мастурбировать',
             'член', 'очко', 'залупа',
             'елда', 'хуесос', 'тварь', 'уебок', 'уебище', 'мудак', 'мудила', 'уебан', 'жопа', 'пизда', 'свастика',
             'гитлер', 'цыган', 'курва',
             'пидр', 'пидорас', 'ебло', 'ебало', 'ебать', 'анал', 'анус', 'ебал', 'сосать', 'говно']


def word_morphy(word):
    parsed_word = morph.parse(word)[0]
    normal_form = parsed_word.normal_form

    return normal_form


def generate_mute(time: int):
    dt = datetime.now() + timedelta(minutes=time)
    time = dt.timestamp()

    return time


