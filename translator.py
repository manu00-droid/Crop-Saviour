from googletrans import Translator


def translation(text, language):
    if language.casefold() == "hindi":
        language = "hi"
    elif language.casefold() == "punjabi":
        language = "pa"
    else:
        language = "en"

    translator_obj = Translator(service_urls=['translate.googleapis.com'])
    result = translator_obj.translate(text, dest=language).text
    return result

