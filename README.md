![Header](https://github.com/ray-MADS/Capstone_jnr_fakenews/blob/master/images/github-header-image%20(8).png)

# Dashboarding Political Bias Misinformation in News Media
## Background 
Political bias and misinformation have always been found in the news media. In recent years, the divide between news outlets based on politics in the US has widened, especially as a result of the recent elections and the global COVID-19 pandemic, influencing the masses. Political researchers and COVID-19 researchers have been challenged with identifying the misinformation in the articles released by the media, as it has become increasingly difficult to identify what would constitute as misinformation. Because of this, an array of methodologies have been developed, and are still being researched, to forward the process in defining misinformation (Cacciatore, 2021). Building systems that can reliably identify misinformation presents an additional challenge for data scientists, as indicators of misinformation may be domain specific. In other words, word and tone usage that indicate misinformation within the political domain may differ from those that indicate misinformation in the health domain (Nan et al., 2021).

In this project, we attempt to build a dashboard that will allow users to explore the relationship between language content, political bias, and misinformation in news articles. Specifically, our web-based dashboard allows for the exploration of the characteristics of political bias misinformation and latent clusters. 

### Data Used 
Two datasets were used in this project. For political bias modeling, we used the “Quantifying News Media Bias Through Crowdsourcing and Machine Learning” dataset, developed by Ceren Budak, Sharad Goel, and Justin M. Rao (2016), accessed from DeepBlue. The dataset includes about 21,000 news articles, with labels based on whether they portray Republican or Democratic policies or politicians positively or negatively. These labels include: Negative, Somewhat Negative, Neutral, Somewhat Positive, and Positive, for both parties. The dataset also includes URLs for each article, of which 15,480 are still accessible for reading. 

For misinformation modeling, we used the “MisInfo Text” dataset, developed by Torabi Asr and Taboada (2019), accessed from GitHub. This dataset includes 1380 news articles, labeled by Buzzfeed “Fact-Checkers” as: Mostly False, a Mix of True and False, and Mostly True. 


## Methods
Before creating the final dashboard, there were a few steps we had to take, namely: 
* Data cleaning
* Exploratory Data Analysis
* Political Bias Modeling and Misinformation Modeling

### Data Cleaning 
The cleaning process for both datasets consisted of the standard NLP methods: tokenizing the articles through stemming and lemmatization. 

### Exploratory Data Analysis (EDA)
The main aspects of our EDA include sentiment analysis and WordCloud creation. 
Using sentiment analysis (via the TextBlob library), we attempted to find if the articles included in Budak et. al's dataset showed any varying sentiment, and, if it did, we would ad sentiment as a feature in our final misinformation model. We found that the majority of models had neutral sentiment polarity, so we did not include it in the final modeling process. 

Because the sentiment analysis did not provide significant information, we turned our attention to the words used in the articles. Using the WordCloud library, we created WordClouds showcasing the top 50 words for all artticles, the articles that lean left, the articles that lean center, and the articles that lean right. 

(insert word cloud pics here)

Through these WordClouds, we found that there were words still present within the tokens that were not handled by NLTK's stopwords list. We appended the words we felt were insignificant (and appeared in the articles over 2000 times) to the stopwords list for further removal and cleaning. 

### Political Bias Modeling and Misinformation Modeling
Our political bias modeling is the basis for our misinformation model. We perform feature engineering by first training a model of political bias. We then apply this model to Torabi Asr and Taboada's dataset containing labeled articles with various levels of misinformation. Using the "new" dataset, we performed K-means clustering analysis with 3 clusters and used the resultant clusters as an additional feature for the misinformation model. The only additional features used to train all models was vectorized article text. 

For our misinformation classification mode, we used a technique for classifying an ordinal label described by Frank & Hall (2001). We explored a Random Forest classifier as well as an AdaBoost classifier. We found the best model performance through the use of a Random Forest classifier for the political bias model and an AdaBoost classifier for the misinformation model.

## The Final Dashboard
Our dashboard is separated into two sections: Data Exploration with our Politcal Bias model, and Misinformation Modeling. 
The Data Exploration section allows for the exploration of a subsample of data from a study by Budak, Goel, & Rao (2016). The study aimed to model political bias from over 20k news articles. We were able to obtain about 15k of these articles. We used ordinal classification to classify articles on a range from 'Strongly Favors Democrats' to 'Strongly Favors Republicans'. The table on the right half displays a list of the article headlines within your selection.

The Misinformation Modeling Section focuses on our evaluation of a dataset containing articles which have been labeled on a three-point ordinal scale: Mostly False, a Mix of True and False, and Mostly True. Data were obtained from a 2019 study by Asr and Taboada, and consisted of 1,380 news articles obtained from Buzzfeed fact checkers. We performed a k-means clustering analysis, and used predicted political bias, predicted clusters, and article text in an ordinal classification model to predict the probability of an article being mostly true, mostly false, or a mix of true and false. The data shown below indicate our model's prediction of an article's veracity, but true labels are also indicated. The table on the right half displays the first 200 characters of all articles within your selection.


[Click here to See Our Dashboard](https://mi-jns.herokuapp.com/)

![Dashboard_A](https://github.com/ray-MADS/Capstone_jnr_fakenews/blob/master/images/newplot4.png)

![Dashboard_A](https://github.com/ray-MADS/Capstone_jnr_fakenews/blob/master/images/newplot5.png)
