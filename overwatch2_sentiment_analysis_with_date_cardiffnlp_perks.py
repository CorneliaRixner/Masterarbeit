import pandas as pd
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import spacy
import torch

# spaCy-Modell laden
nlp = spacy.load("en_core_web_sm")

# RoBERTa-Tokenizer und Modell laden
tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Bereinigte CSV-Datei laden
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_data_cleaned_update_perks_with_date.csv"
output_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_data_with_sentiment_perks_with_date.csv"

df = pd.read_csv(input_file)

# Debugging: Beispielwerte aus der Datei anzeigen
print("Beispielwerte aus der Datei:")
print(df.head())

# Spalte 'created' sichern und aus dem DataFrame entfernen
created_column = df['created']
df = df.drop(columns=['created'])

# Leere Werte in 'body_clean' durch leere Strings ersetzen und sicherstellen, dass alle Werte Strings sind
df['body_clean'] = df['body_clean'].fillna("").astype(str)
print("Beispielwerte aus 'body_clean':", df['body_clean'].head())

# Funktion zur Sentimentanalyse
def analyze_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return "neutral"  # Rückgabe eines Standardwerts für leere oder ungültige Texte

    try:
        # Tokenisierung und Modellvorhersage
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        logits = outputs.logits
        sentiment_class = torch.argmax(logits, dim=1).item()

        # Mapping der Klassen
        sentiment_map = {0: "negativ", 1: "neutral", 2: "positiv"}
        return sentiment_map[sentiment_class]
    except Exception as e:
        print(f"Fehler bei der Verarbeitung des Textes: {text}. Fehler: {e}")
        return "neutral"

# Sentimentanalyse auf die Spalte 'body_clean' anwenden
print("Starte Sentimentanalyse...")
df['sentiment'] = df['body_clean'].apply(analyze_sentiment)

# Spalte 'created' wieder hinzufügen
df['created'] = created_column

print(df['sentiment'].value_counts())

# Ergebnisse speichern, einschließlich der Datumsspalte
df[['created', 'title_clean', 'body_clean', 'sentiment']].to_csv(output_file, index=False)
print("Sentimentanalyse abgeschlossen. Ergebnisse gespeichert unter:", output_file)