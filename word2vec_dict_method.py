from gensim.models import Word2Vec
import All_Functions as af

def get_similar_words(rd_file, shooter_name):
    content = af.import_csv(rd_file)
    event_name = af.get_event_name(rd_file)
    sentences = [] # check that it gets the event name correctly
    for i in range(len(content)):
        if content[i][-2] == '1' and content[i][-1] == '1':  # true positives
            sentences.append(content[i][10])
        if content[i][-2] == '1' and content[i][-1] == 'None':  # dict positives
            sentences.append(content[i][10])
        if content[i][-2] == '0' and content[i][-1] == '1':  # false negatives
            sentences.append(content[i][10])

    model = Word2Vec(sentences=sentences, window=5, min_count=1, workers=4)
    try:
        related = model.wv.most_similar(shooter_name, topn=25)
        print(f"Here are the most similar words to {shooter_name} in the {event_name} file:")
        print(related)
    except KeyError:
        try:
            loc = event_name.split()
            related = model.wv.most_similar(loc[0], topn=25)
            print(f"Here are the most similar words to {loc[0]} in the {event_name} file:")
            print(related)
        except KeyError:
            print('Neither the location nor the shooter name are present in the file')
# print(str(x[0]) for x in related)

