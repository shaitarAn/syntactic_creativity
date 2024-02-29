import re
import string

def preprocess_text(source_text, lang):
    if lang == "ja":
        source_text = normalize_japanese_punct(source_text)
    elif lang == "de":
        source_text = normalize_german_punct(source_text)

    else:               
        source_text = normalize_punct(source_text)
    source_text = capitalize_after_period_space(source_text)

    return source_text

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

def insert_space_after_period(text):
    # Define the pattern to match a period followed by a character or a digit
    pattern = r'(\.)([^\s])'

    # Define a function to replace matches with the pattern
    def repl_func(match):
        return match.group(1) + ' ' + match.group(2)

    # Use re.sub() to replace matches in the text with space after the period
    return re.sub(pattern, repl_func, text)

def is_only_punctuation(text):
    additional_punctuation = "」。"  # Add the characters you want to include here
    if all(char in string.punctuation or char in additional_punctuation for char in text.strip()):
        return True
    
def has_digit(text):
    if text.strip().replace(".", "").isdigit() or text.strip().replace(")", "").isdigit():
        return True

def remove_html_chars(text):
    text = text.replace("<unintelligible/>", "")
    text = text.replace("<unverständlich/> ", "") 
    text = text.replace("<Unverständlich/>", "")
    text = text.replace("<parallel_talk>", "")
    text = text.replace("</parallel_talk>", "")
    # text = text.replace("<laugh/>", "")
    # text = text.replace("*lacht*", "")
    return text

def remove_mt_artifacts(text):
    text = text.replace("Sorry, but I am unable to translate an unintelligible text. If you provide a clear text in English, I will be happy to help you with the translation into German.", "") # 4 occurences in de-en gpt3
    text = text.replace("Sorry, but I am unable to provide a translation without the actual text. Could you please provide the exact text that needs to be translated?", "") # 12 occurences in de-en gpt3
    text = text.replace("Translate the following text into German. Output only the translation itself without additional commentary or explanations. Text: ", "") # 68 occurences in en-de_news.gpt3!
    text = text.replace("Translate the following text into German. Output only the translation itself without additional commentary or explanations.  Text: ", "")
    text = text.replace("Could you please provide the text you want me to translate?", "") # 1 time in en-de gpt4
    text = text.replace("As a translator, I need the text to be translated. Currently, the text """, "")
    text = text.replace('"" is not providing any content to be translated to German. Please provide the necessary details.', "") # 8 occurences de-en gpt4 for sentences like (PERSON#)
    text = text.replace("You need to provide a text for translation.", "(PERSON1)")
    text = text.replace("Could you please provide the text you want me to translate?", "1)")
    text = text.replace("The target text includes a German translation of the source text. The German translation is: ", "")
    text = text.replace("The German translation of the source text is:", "")
    text = text.replace("The text translates to: ", "")
    text = text.replace("The text you provided (""1"") does not need to be translated as it is a numeral, which stays the same in both German (de) and English (en).", "1")
    text = text.replace("\n", "")
    text = text.replace("The English translation is: ", "")
    text = text.replace('"Okay" kann auf Deutsch als "in Ordnung" oder "okay" übersetzt werden.', "Okay")
    
    return text

def split_sentences(reader, lang, wtp, col=int):
    # Define a variable to store the buffer
    punctuation_buffer = ""

    sentences = []

    for row in reader:
        text = row[col]
       
        text = preprocess_text(text, lang)
        text = capitalize_after_period_space(text) 
        text = insert_space_after_period(text)  

        # split texts into sentences
        source_sents = wtp.split(text, lang_code=lang, style="ud")

        for sent in source_sents:
            sent = sent.replace("\n", " ")
            sent = sent.lstrip()

            if has_digit(sent):
                # Append the punctuation-only line to the buffer
                punctuation_buffer += sent.strip() + " "
            elif is_only_punctuation(sent):
                continue
            else:
                # If the current line is not punctuation-only, write the buffer and reset it
                if punctuation_buffer:
                    sent = punctuation_buffer + sent
                    punctuation_buffer = ""

                sentences.append(sent.strip())


    # Write any remaining content in the buffer to the output files
    if punctuation_buffer:
        sentences.append(sent.strip())

    return sentences

# # Example text
# text = "High seat three. village. another example. here."

# # Preprocess the text
# processed_text = capitalize_after_period_space(text)

# print(processed_text)
