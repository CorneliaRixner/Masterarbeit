import pandas as pd
import re

# Dateipfad anpassen
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_reddit_knaggle_prepared_3.csv"
output_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_reddit_knaggle_cleaned_with_date.csv"

# CSV einlesen
df = pd.read_csv(input_file)

# Debug: Spaltennamen anzeigen
print("Spaltennamen:", df.columns.tolist())

# Emoji Bereich U+1F600 - U+1F64F
emoji_pattern = re.compile("[\U0001F600-\U0001F64F]")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'http\S+', '', text)  # URLs entfernen
    text = emoji_pattern.sub(lambda x: f" {x.group()} ", text)  # Emojis als Platzhalter sichern
    text = re.sub(r'[^a-zA-Z0-9#\s\U0001F600-\U0001F64F]', '', text)  # Sonderzeichen entfernen
    text = re.sub(r'\s+', ' ', text).strip()  # Mehrfache Leerzeichen bereinigen
    return text

# Bereinigen der relevanten Spalten
df['post_title_clean'] = df['post_title'].apply(clean_text)
df['comment_body_clean'] = df['comment_body'].apply(clean_text)

# Nur die gewünschten Spalten exportieren
df[['comment_date', 'post_title_clean', 'comment_body_clean']].to_csv(output_file, index=False)
print("Bereinigte Datei gespeichert unter:", output_file)
