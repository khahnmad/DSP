import All_Functions as af
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# Import number of correctly classified articles
classified_articles = [x for x in glob.glob('evaluations' + "/*.csv")]

complete_locations = [[],[]] # keep track of each of the events so i don't import an event twice
# all_classified_text = []
for file in classified_articles:
    location = af.get_event_name(file)
    best_classification = 'evaluations\\'+location+'_3-eval.csv' # using round 3 since it's most often reliable, this could be improved
    if location not in complete_locations[0]: # if we haven't already imported this event
        if best_classification in classified_articles: # get round 3 if possible
            classified_text = af.import_csv(best_classification)
            # all_classified_text.append(classified_text)
            positives = int(classified_text[1][0])-int(classified_text[1][2])+int(classified_text[1][2]) # positives - fps + fns
            complete_locations[0].append(location)
            complete_locations[1].append(positives)
        elif best_classification not in classified_articles:
            if  location+'_round-2.csv' in classified_articles: # otherwise try round 2
                classified_text = af.import_csv('evaluations'+location+'_2-eval.csv')
                # all_classified_text.append(classified_text)
                positives = int(classified_text[1][0])-int(classified_text[1][2])+int(classified_text[1][2])  # positives - fps + fns
                complete_locations[0].append(location)
                complete_locations[1].append(positives)
            else: # otherwise try round 1
                classified_text = af.import_csv(file)
                # all_classified_text.append(classified_text)
                positives = int(classified_text[1][0])-int(classified_text[1][2])+int(classified_text[1][2])  # positives - fps + fns
                complete_locations[0].append(location)
                complete_locations[1].append(positives)

# Import number of victims for each shooting
shooting_db = af.import_csv('generate-sample/intial-sample-w-info.csv')

# change the event name formatting
for i in range(len(complete_locations[0])):
    if "_" in complete_locations[0][i]:
        complete_locations[0][i]=complete_locations[0][i].replace("_", " ")

# collect the number of fatalities per shooting & relationship between victim & shooter
complete_locations.append([None for x in range(len(complete_locations[0]))])
complete_locations.append([None for x in range(len(complete_locations[0]))])
for i in range(len(complete_locations[0])):
    for j in range(len(shooting_db)):
        if complete_locations[0][i]==shooting_db[j][3]:
            complete_locations[2][i] = int(shooting_db[j][6])
            complete_locations[3][i] = int(shooting_db[j][7])


# Output: Scatter plot with x-axis # killed and y-axis # of articles, color = known/unknown & label for each shooting
y = complete_locations[1] # number of articles
x = complete_locations[2] # number killed
labels = complete_locations[0] # labels
hue = complete_locations[3] # relationship between victim and perp

X = np.array(x).reshape(-1, 1)
reg = LinearRegression().fit(X, y)
art_killed_score = reg.score(X,y)

lr_x = x
lr_y = reg.predict(np.array(X))

fig, ax = plt.subplots()
ax.scatter(x, y ,c=hue)
ax.plot(lr_x, lr_y)
ax.set_title("Shootings' Number of Articles and Number of Fatalities")
ax.set_ylabel('# of Articles about the Shooting')
ax.set_xlabel('# of Fatalities')
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))

plt.show()



