import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
import spacy

# CSV einlesen
input_file = r"C:\Users\conri\Documents\FIT Master\5. Semester\Masterarbeit\03_Datensätze\Reddit-Beiträge\Covid 19\covid_19_kaggle_topic_modeling_tokenized_lemmatized_no_stopwords.csv"
df = pd.read_csv(input_file)

# Nur Zeilen ohne NaN in lemmas_no_stopwords verwenden
df_valid = df[df['lemmas_no_stopwords'].notna()].copy()
texts = df_valid['lemmas_no_stopwords'].astype(str).tolist()

# Tokenisierung
tokenized_texts = [text.split() for text in texts]

# Dictionary und Korpus für gensim
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# LDA-Modell trainieren
num_topics = 8 
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=8)
lda_model.save("covid_19_lda_model")
dictionary.save("covid_19_lda_dictionary")

# Topics ausgeben
for idx, topic in lda_model.print_topics(num_words=8):
    print(f"Topic {idx+1}: {topic}")

# Zuweisung der Top-Topics zu jedem Dokument
df_valid['topic'] = [max(lda_model[doc], key=lambda x: x[1])[0] if lda_model[doc] else None for doc in corpus]
output_file = input_file.replace('.csv', '_with_topics.csv')
df_valid.to_csv(output_file, index=False)
print(f"Datei mit Topic-Zuordnung gespeichert unter: {output_file}")
