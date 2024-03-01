# medieval_guilds

This project contains all the scripts created for my thesis Guilds in Italy during the 12th-18th century : An Empirical Approach. The thesis aimed at collecting data from three different sources : two excel databases and one digitalized catalog. The challenge was to create a unique datasets. The data have been used to produce relevant graphs and tables to give an overview of the guilds' presence in Italy in the considered period. Further, the data have been used to empirical test the hypothesis that the medieval guilds had a postive impact on economic growth. 
From a coding perspective the main challenges have been:
-using web scraping and text analysis tools to sequentially download the PDFs of the Chelazzi Catalog and analyze the files to extract the relevatn information abouth name, place and years of the guilds. Then create an excel datasets with these information;
-trying to create a unique dataset merging the information on the two database and the new created one. In this case, text analysis tools were used to peform merging when the name of the guild was not clearly the same, but similar;
-several scripts regard data management and visualization, which have been extensively used to represent the data produced with the created dataset;
-finally the scripts in R and STATA are the one used to perform the empirical analysis part. 
