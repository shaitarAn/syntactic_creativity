from langdetect import detect

translation_into = {"en": "<Translation into English>", "pl": "<Tłumaczenie na język polski>", "ja": "<日本語への翻訳>", "de": "<Übersetzung ins Deutsche>"}

lang_instructions = {
    "en": "Now read this source text: <Beginning of source text>  {source_text} <End of source text>. Finally, translate it into English: <Translation into English>", 
    "pl": " Teraz przeczytaj ten tekst źródłowy: <początek tekstu źródłowego> {source_text} <koniec tekstu źródłowego>. Na koniec przetłumacz go na język polski: <Tłumaczenie na język polski>", 
    "ja": "では、この原文を読んでみましょう： <原文の始まり> {source_text} <原文の終わり>。最後に、これを日本語に翻訳します： <日本語への翻訳>", 
    "de": "Lies nun diesen Ausgangstext: <Anfang des Quelltextes> {source_text} <Ende des Quelltextes>. Übersetze ihn schließlich ins Deutsche: <Übersetzung ins Deutsche>"}

promptline_dict = {
    "en": 
    """<Beginning of source text> {source_text} <End of source text>. Here is a bad translation into English: <Beginning of translation> {translations} Translate the source text into English. Learn from this example: <Beginning of source text> {examplein} <End of source text>; <Beginning of translation> {exampleout} <End of translation>. Now read this source text: <Beginning of source text>  {source_text} <End of source text>. Finally, translate it into English: <Beginning of translation>"""}

translations = ["<Translation into English>", "<Tłumaczenie na język polski>", "<日本語への翻訳>", "<Übersetzung ins Deutsche>"]

['"Tata, I like grilled chicken, so let\'s grill it today and eat it," I said, repeating the words clearly, but Mother didn\'t seem to hear them well. She was startled, and the other children\'s mothers nearby were also surprised. They opened their eyes and mouths wide in surprise, making a strange face. I felt like laughing, but then I saw the person looking at my hand and thought, "Oh, it\'s not enough."', 
'',
'"More, more, more!" I said, looking at the sparrows walking nearby. Mother called out to me in a voice that sounded like she was about to cry, "Akiko! Don\'t do that! The birds are going to build a nest and lay eggs. Everyone is crying. Your friends are dead and it\'s lonely. It\'s sad, isn\'t it?"',
'',
'"Why? They\'re already dead," I asked, questioning Mother\'s words. She was at a loss for words.']

import json
# check if any translation is in the target language if translation is not empty string
with open("promptlines.json", "r") as f:
    plines = json.load(f)
    prompttype = plines["KarpinskaPromptline"]["name"]
    promptlines = plines["KarpinskaPromptline"]["promptline"]

    print(prompttype)
    print(promptlines)


