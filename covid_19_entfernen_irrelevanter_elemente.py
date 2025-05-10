import pandas as pd
import re

input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_reddit_knaggle_prepared.csv"
output_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_reddit_knaggle_cleaned.csv"

# CSV laden
df = pd.read_csv(input_file)

# Nur "body" Spalte nutzen und NaN entfernen
df = df[['body']]
df = df.dropna(subset=['body'])

# Nur echte Kommentare behalten
df = df[df['body'].apply(lambda x: str(x).count(",") < 2)]

# Emoji Bereich
emoji_pattern = re.compile("[\U0001F600-\U0001F64F]")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'http\S+', '', text)
    text = emoji_pattern.sub(lambda x: f" {x.group()} ", text)
    text = re.sub(r'[^a-zA-Z0-9#\s\U0001F600-\U0001F64F]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Bereinigen
df['body_clean'] = df['body'].apply(clean_text)

# NEU: Leere bereinigte Kommentare entfernen
df = df[df['body_clean'].str.strip() != ""]

# Vorschau
print(df[['body', 'body_clean']].head())

# Speichern
df.to_csv(output_file, index=False)
print("Bereinigte Datei gespeichert unter:", output_file)







