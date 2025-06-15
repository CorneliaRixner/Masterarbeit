import pandas as pd
import spacy
import os

# CSV einlesen
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_topic_modeling_fulltext.csv"
df = pd.read_csv(input_file)

print("Anzahl Zeilen:", len(df))
print("Null-Werte in full_text:", df['full_text'].isnull().sum())

# Lade spaCy-Modell
print("Lade spaCy-Modell...")
nlp = spacy.load("en_core_web_sm")

# Tokenisierung mit spaCy
def spacy_tokenize(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    doc = nlp(text)
    return ' '.join([token.text for token in doc if not token.is_punct and not token.is_space])

token_list = []
for idx, text in enumerate(df['full_text']):
    if idx % 100 == 0:
        print(f"Tokenisiere Zeile {idx} von {len(df)}")
    try:
        token_list.append(spacy_tokenize(text))
    except Exception as e:
        print(f"Fehler beim Tokenisieren in Zeile {idx}: {e}")
        token_list.append("")

df['tokens'] = token_list
print("Tokenisierung abgeschlossen")

# Nach Tokenisierung speichern
output_file_tokens = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_topic_modeling_fulltext_tokenized.csv"
df.to_csv(output_file_tokens, index=False)
print(f"Datei nach Tokenisierung gespeichert unter: {output_file_tokens}")

# Lemmatisierung mit spaCy
def spacy_lemmatize(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_punct and not token.is_space])

lemma_list = []
for idx, text in enumerate(df['tokens']):
    if idx % 100 == 0:
        print(f"Lemmatisiere Zeile {idx} von {len(df)}")
    try:
        lemma_list.append(spacy_lemmatize(text))
    except Exception as e:
        print(f"Fehler beim Lemmatisieren in Zeile {idx}: {e}")
        lemma_list.append("")

df['lemmas'] = lemma_list
print("Lemmatisierung abgeschlossen")

# Nach Lemmatisierung speichern
output_file_lemmas = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_topic_modeling_fulltext_tokenized_lemmatized.csv"
df.to_csv(output_file_lemmas, index=False)
print(f"Datei nach Lemmatisierung gespeichert unter: {output_file_lemmas}")

# Stoppwörter entfernen
stopwords = nlp.Defaults.stop_words
print(f"Anzahl Stoppwörter: {len(stopwords)}")

def remove_stopwords(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    return ' '.join([word for word in text.split() if word.lower() not in stopwords])

no_stopword_list = []
for idx, text in enumerate(df['lemmas']):
    if idx % 100 == 0:
        print(f"Entferne Stoppwörter in Zeile {idx} von {len(df)}")
    try:
        no_stopword_list.append(remove_stopwords(text))
    except Exception as e:
        print(f"Fehler beim Entfernen der Stoppwörter in Zeile {idx}: {e}")
        no_stopword_list.append("")

df['lemmas_no_stopwords'] = no_stopword_list
print("Stoppwörter entfernt")

# Nach Entfernen der Stoppwörter speichern
output_file_no_stopwords = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_topic_modeling_fulltext_tokenized_lemmatized_no_stopwords.csv"
df.to_csv(output_file_no_stopwords, index=False)
print(f"Datei nach Entfernen der Stoppwörter gespeichert unter: {output_file_no_stopwords}")

# Stoppwortliste speichern
stopword_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\spacy_stopwords.txt"
with open(stopword_file, "w", encoding="utf-8") as f:
    for word in sorted(stopwords):
        f.write(word + "\n")
print(f"Stoppwortliste gespeichert unter: {stopword_file}")

print("Alle Verarbeitungsschritte abgeschlossen.")