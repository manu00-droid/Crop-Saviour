from googletrans import Translator


def translation(text, language):
    translator_obj = Translator(service_urls=['translate.googleapis.com'])
    result = translator_obj.translate(text,
                                      dest=language).text
    return result
