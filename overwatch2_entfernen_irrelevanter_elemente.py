import pandas as pd
import re

file_name = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_data_update_perks.csv"

# CSV laden
df = pd.read_csv(file_name)

# Emoji Bereich U+1F600 - U+1F64F
emoji_pattern = re.compile("[\U0001F600-\U0001F64F]")

def clean_text(text):
    if pd.isna(text):
        return ""

    # URLs entfernen
    text = re.sub(r'http\S+', '', text)

    # Emojis als Platzhalter sichern
    text = emoji_pattern.sub(lambda x: f" {x.group()} ", text)

    # Sonderzeichen entfernen (alles außer Buchstaben, Zahlen, Hashtags, Emojis und Leerzeichen)
    text = re.sub(r'[^a-zA-Z0-9#\s\U0001F600-\U0001F64F]', '', text)

    # Mehrfache Leerzeichen bereinigen
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Bereinigen der relevanten Spalten
df['body_clean'] = df['body'].apply(clean_text)
df['title_clean'] = df['title'].apply(clean_text)

# Vorschau der bereinigten Daten
print(df[['created', 'title_clean', 'body_clean']].head())

# Speichern der bereinigten Datei mit der ersten Spalte als Datum
output_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_data_cleaned_update_perks_with_date.csv"
df[['created', 'title_clean', 'body_clean']].to_csv(output_file, index=False)
print("Bereinigte Datei gespeichert unter:", output_file)



