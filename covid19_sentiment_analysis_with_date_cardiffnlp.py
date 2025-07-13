import pandas as pd
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

# Modell und Tokenizer laden
tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Eingabedatei und Ausgabedatei
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_knaggle_cleaned_with_date.csv"
output_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_knaggle_sentiment.csv"

# CSV einlesen
df = pd.read_csv(input_file)

def analyze_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return "neutral"
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        logits = outputs.logits
        sentiment_class = torch.argmax(logits, dim=1).item()
        sentiment_map = {0: "negativ", 1: "neutral", 2: "positiv"}
        return sentiment_map[sentiment_class]
    except Exception as e:
        print(f"Fehler bei der Verarbeitung des Textes: {text}. Fehler: {e}")
        return "neutral"

# Sentimentanalyse anwenden
print("Starte Sentimentanalyse...")
df['sentiment'] = df['comment_body_clean'].apply(analyze_sentiment)

# Ergebnis speichern
df.to_csv(output_file, index=False)
print("Sentimentanalyse abgeschlossen. Ergebnisse gespeichert unter:", output_file)
