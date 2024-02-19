import re

def normalize_punct(line):
    line = line.replace(" ’", "")
    line = line.replace("’", "'")
    line = line.replace("?'", "?")
    line = line.replace("!'", "!")
    line = line.replace(".'", ".")
    line = line.replace(",'", ",")
    line = line.replace(":'", ":")
    line = line.replace("—'", ". ")
    line = line.replace("„", '"')
    line = line.replace("“", '"')
    line = line.replace("”", '"') 
    line = line.replace("‘","")
    line = line.replace("……", "。")
    line = line.replace("…", ".")
    line = line.replace("......", ".")
    line = line.replace(" . . .", ".")
    line = line.replace("– ", "")
    line = line.replace("— ", "")
    line = line.replace("- ", "")
    line = line.replace("— ", "")
    line = line.replace(" ?", "?")
    line =line.replace(" !", "!")

    return line

def normalize_german_punct(line):
    line = line.replace("«", '"')
    line = line.replace("»", '"')
    line = line.replace('?" ', '"? ')
    line = line.replace('." ', '". ')
    line = line.replace('!" ', '"! ')

    return line

def normalize_japanese_punct(text):
    text = text.replace("．", "。")
    text = text.replace(".", "。")
    # text = text.replace("！", "!")
    # text = text.replace("？", "?")
    text = text.replace("。", "。")
    # text = text.replace("」", " ")
    # text = text.replace("「", " ")
    return text

def capitalize_after_period_space(text):

    def repl_func(match):
        return match.group(1) + match.group(2).upper()

    pattern = r'(\w\. )([a-z])'
    return re.sub(pattern, repl_func, text)


def remove_html_chars(text):
    text = text.replace("<", "")
    text = text.replace("/>", "")
    return text


def clean_text(text):
    text = text.replace("Sorry, but I am unable to translate an unintelligible text. If you provide a clear text in English, I will be happy to help you with the translation into German.", "<unintelligible>") # 4 occurences in de-en gpt3
    text = text.replace("Translate the following text into de. Output only the translation itself without additional commentary or explanations. Text: ", "") # 68 occurences in en-de_news.gpt3!
    text = text.replace("Translate the following text into de. Output only the translation itself without additional commentary or explanations.  Text: ", "")
    text = text.replace("Could you please provide the text you want me to translate?", "") # 1 time in en-de gpt4
    text = text.replace("As a translator, I need the text to be translated. Currently, the text """, "")
    text = text.replace('"" is not providing any content to be translated to German. Please provide the necessary details.', "") # 8 occurences de-en gpt4 for sentences like (PERSON#)
    text = text.replace("You need to provide a text for translation.", "(PERSON1)")
    text = text.replace("Could you please provide the text you want me to translate?", "1)")
    text = text.replace("The target text includes a German translation of the source text. The German translation is: ", "")
    text = text.replace("The German translation of the source text is:", "")
    text = text.replace("The text translates to: ", "")
    text = text.replace('The text you provided ("1") does not need to be translated as it is a numeral, which stays the same in both German (de) and English (en).', "1")
    text = text.replace("\n", "")
    text = text.replace("1. 1. 1 1.", "")
    text = text.replace(" 1. 1. 1. 1.","")
    
    return text

# # Example text
# text = "High seat three. village. another example. here."

# # Preprocess the text
# processed_text = capitalize_after_period_space(text)

# print(processed_text)
