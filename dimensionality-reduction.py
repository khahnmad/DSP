# Imports
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import All_Functions as af
import pandas as pd
from sklearn.cluster import KMeans


# FUNCTIONS
def visualize_dr(file):
    content = af.import_csv(file) # import file with tf-idf matrix

    pca = PCA(n_components=2) # 2 components for a 2-d visualization
    principalComponents = pca.fit_transform(content)
    # convert to pandas for easy scatterplot
    principalDf = pd.DataFrame(data= principalComponents, columns = ['principal component 1', 'principal component 2'])
    principalDf.plot.scatter(x='principal component 1',y='principal component 2')
    plt.show()


def reduce_dimensionality(file, components):
    content = af.import_csv(file)  # import file with tf-idf matrix
    pca = PCA(n_components=components)
    return pca.fit_transform(content)


# k-means


aurora_rd = reduce_dimensionality('tf-idf-scores/Aurora-2_tf-idf.csv', 5)
kmeans = KMeans(n_clusters=2, random_state=0).fit(aurora_rd)
# kmeans.labels_
aurora_cleaned = af.import_csv('Aurora_round_2.csv')



headlines = [x[2] for x in aurora_cleaned[1:]]
dict_class = [x[-2] for x in aurora_cleaned[1:]]
labels = list(kmeans.labels_)
data = []
for i in range(len(headlines)):
    data.append([headlines[i],dict_class[i], labels[i]])

df = pd.DataFrame(columns=['headlines','dict label','cluster label'], data=data)
# df = pd.DataFrame(data=data)
print('checkpoint')