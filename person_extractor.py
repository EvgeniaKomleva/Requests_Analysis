import re

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsNERTagger,
    NamesExtractor,
    NewsSyntaxParser,
    Doc
)
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
result_per = {}

# -*- coding: latin-1 -*-


lines = ['справка от Иванова Павла Петровича и Марии Николаевны']

def person_extract(line, str_num, id):
    all_result_per = {"Author" : []}
    result_per = {}
    persons = {}
    temp_me = {}
    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    ner_tagger = NewsNERTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    names_extractor = NamesExtractor(morph_vocab)
    doc = Doc(line)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    doc.parse_syntax(syntax_parser)
    person_id = 1
    for span in doc.spans:
        span.normalize(morph_vocab)
        name , surname, patronymic_name = '','', ''

        if span.type == 'PER':
            span.extract_fact(names_extractor)
            temp = {}
            temp["id"] = str(id)
            #id = id + 1
            try:

                name = span.fact.as_dict['first']
                p = morph.parse(name)[0]
                if p.tag.case != 'gent':
                    #return all_result_per, id
                    continue
                name = p.normal_form
                firstname = [
                    {
                        "value": name,
                        "annotations": {
                            "annotationStart": span.start,
                            "annotationEnd": span.stop,
                            "annotationText": span.text
                        }
                    }
                ]
                temp["firstname"] = firstname
            except:
                pass

            try:
                surname = span.fact.as_dict['last']
                p = morph.parse(surname)[0]
                surname = p.normal_form
                surname = [
                    {
                        "value": surname,
                        "annotations": {
                            "annotationStart": span.start,
                            "annotationEnd": span.stop,
                            "annotationText": span.text
                        }
                    }
                ]
                temp["surname"] = surname
            except:
                pass

            try:
                patronymic_name = span.fact.as_dict['middle']

                p = morph.parse(patronymic_name)[0]
                patronymic_name = p.normal_form
                patronymic_name = [
                    {
                        "value": patronymic_name,
                        "annotations": {
                            "annotationStart": span.start,
                            "annotationEnd": span.stop,
                            "annotationText": span.text
                        }
                    }
                ]
                temp["patronymic_name"] = patronymic_name
            except:
                pass

            # temp ={
            #     #"id": person_id,
            #     #"line": line,
            #     "id": id,
            #     "text": span.text,
            #     "firstname": name,
            #     "surname": surname,
            #     "patronymic_name": patronymic_name,
            #     "annotations": {
            #         "annotationStart": span.start,
            #         "annotationEnd": span.stop
            #         }
            #     }

            #print(result_per)
            #all_result_per.update(result_per)
            #persons["id"] = str(id)
            id =id +1
            #persons["Person"+str(person_id)]=temp

            #temp = {"firstname":firstname, "surname":surname, "patronymic_name":patronymic_name}
            all_result_per["Author"].append(temp)
            person_id = person_id + 1
            #if span.text.find("мои ") or span.text.find("мой ") or span.text.find("моё ") :
            #   result_per["surname"] = '@Me'
        me_pos = 0
    if line.find("мои ") != -1:
        search = re.search("мои ", line)
        text = "мои "
    if line.find("мой ") != -1:
        search = re.search("мой ", line)
        text = "мой "
    if line.find("моё ") != -1:
        search = re.search("моё ", line)
        text = "моё "
    if line.find("мои ") != -1 or line.find("мой ")!=-1 or line.find("моё ")!=-1:
        #map["surname"] = '@Me'
        surname = [
            {
                "value": '@Me',
                "annotations": {
                    "annotationStart": search.start(),
                    "annotationEnd": search.end(),
                    "annotationText": text
                }
            }
        ]
        temp_me["surname"] = surname
        all_result_per["Author"].append(temp_me)
    #all_result_per["Author"] = [persons]

    return all_result_per, id


if __name__ == "__main__":
    for line in lines:
        map = person_extract(line)
        if line.find("мои ") != -1 or line.find("мой ")!=-1 or line.find("моё ")!=-1:
            map["surname"] = '@Me'
        print(map)
