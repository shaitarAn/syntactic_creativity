translation_into = {"en": "<Translation into English>", "pl": "<Tłumaczenie na język polski>", "ja": "<日本語への翻訳>", "de": "<Übersetzung ins Deutsche>"}

lang_instructions = {
    "en": "Now read this source text: <Beginning of source text>  {source_text} <End of source text>. Finally, translate it into English: <Translation into English>", 
    "pl": " Teraz przeczytaj ten tekst źródłowy: <początek tekstu źródłowego> {source_text} <koniec tekstu źródłowego>. Na koniec przetłumacz go na język polski: <Tłumaczenie na język polski>", 
    "ja": "では、この原文を読んでみましょう： <原文の始まり> {source_text} <原文の終わり>。最後に、これを日本語に翻訳します： <日本語への翻訳>", 
    "de": "Lies nun diesen Ausgangstext: <Anfang des Quelltextes> {source_text} <Ende des Quelltextes>. Übersetze ihn schließlich ins Deutsche: <Übersetzung ins Deutsche>"}

promptline_dict = {
    "en": 
    """<Beginning of source text> {source_text} <End of source text>. Here is a bad translation into English: <Beginning of translation> {translations} Translate the source text into English. Learn from this example: <Beginning of source text> {examplein} <End of source text>; <Beginning of translation> {exampleout} <End of translation>. Now read this source text: <Beginning of source text>  {source_text} <End of source text>. Finally, translate it into English: <Beginning of translation>"""}