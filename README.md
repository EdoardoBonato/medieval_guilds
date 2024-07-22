# medieval_guilds

This project contains all the scripts created for my thesis titled _Guilds in Italy during the 12th-18th century : An Empirical Approach_.
The thesis aimed at collecting data from three different sources : two excel databases and one digitalized catalog. This in order to have a clearer general view on guilds' presence in Italy and to invetigate the debated issue on the economic impact of guilds on economic growth. For this last goal, the data have been used to empirical test the hypothesis that the medieval guilds had a postive impact on economic growth. 

**Data Collection and Merging** 

A set of data containing information on guilds' presence in Italy, which have never been used, where sequentially extracted from the Chelazzi Catalog, published by the Italian Senate (unfortunately they keep chaning the URL). After having done that, they were merged with the two existing dataset,  the italian Guilds Database and the Datasets published by Ogilvie for her book. Web Scraping technique and text analysis tools were used to extract the data, to find similarity between guilds' name and to deal with translition of name from English to Italian. The result was the creation of the unique dataset.

**Data Analysis and Investigation** 

The several trends, at the national,regioanl and city-level were deeply explored in the thesis. To do so, several graph were created (with Plotly) together with several descriptive statistics. This aimed at structuring the theoretical proposal which led to the hypothesis of postive impact of guilds in economic growth, thorugh a double effect of improving skills accumulation and creating enforcement system in a period in which, in Italy, a public government coukd have difficultly have done so. 

**Empirical Testing** 

The scripts in STATA and R were used to test the empirical model. Which is, at the national level a Fixed-Effect model, with lagged value of new guilds' by decade as regressors, and economic growth at 10-yrs level as dependent variable. The results were significant. Further, the test at the regional level, which produced mixed findings, was conducted thorugh a simple time series analysis with (detrended) lagged value of guilds' creation on economic growth. 


