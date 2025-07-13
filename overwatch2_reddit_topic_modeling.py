import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
import spacy

# CSV einlesen
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Overwatch2\overwatch2_reddit_topic_modeling_lemmatized_no_stopwords_only.csv"
df = pd.read_csv(input_file)

# Nur die Spalte mit den vorbereiteten Texten verwenden
texts = df['lemmas_no_stopwords'].dropna().astype(str).tolist()

# Tokenisierung (spaCy nicht zwingend nötig, da schon lemmatisiert und stopwords entfernt)
# Wir splitten einfach nach Leerzeichen
tokenized_texts = [text.split() for text in texts]

# Dictionary und Korpus für gensim
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# LDA-Modell trainieren
num_topics = 8 
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=8)
lda_model.save("overwatch2_lda_model")
dictionary.save("overwatch2_lda_dictionary")

# Topics ausgeben
for idx, topic in lda_model.print_topics(num_words=8):
    print(f"Topic {idx+1}: {topic}")

# Optional: Zuweisung der Top-Topics zu jedem Dokument
df['topic'] = [max(lda_model[doc], key=lambda x: x[1])[0] if lda_model[doc] else None for doc in corpus]
output_file = input_file.replace('.csv', '_with_8_topics.csv')
df.to_csv(output_file, index=False)
print(f"Datei mit Topic-Zuordnung gespeichert unter: {output_file}")
