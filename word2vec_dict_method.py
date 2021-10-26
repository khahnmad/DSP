from gensim.models import Word2Vec
import All_Functions as af

def get_similar_words(rd_file, shooter_name):
    content = af.import_csv(rd_file)

    sentences = []
    for i in range(len(content)):
        if content[i][-2] == '1' and content[i][-1] == '1':  # true positives
            sentences.append(content[i][10])
        if content[i][-2] == '1' and content[i][-1] == 'None':  # dict positives
            sentences.append(content[i][10])
        if content[i][-2] == '0' and content[i][-1] == '1':  # false negatives
            sentences.append(content[i][10])
    model = Word2Vec(sentences=sentences, window=5, min_count=1, workers=4)
    # model.save("word2vec.model")

    model = Word2Vec.load("word2vec.model")
    related = model.wv.most_similar(shooter_name, topn=25)
# print(str(x[0]) for x in related)
    event_name = af.get_event_name(rd_file)
    print(f"Here are the most similar words to {shooter_name} in the {event_name} file:")
    print(related)