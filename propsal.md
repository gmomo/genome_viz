## Canadian Centre for Computational Genomics - GsoC 2019 Proposal

### Project Info

#### Human history and data visualization
The goal of this project is to create an easy-to-use python pipeline to produce such data visualizations from genomic data. The data needs to be dimensionally reduced to 2/3 dimensions using either PCA,UMAP,t-SNE or a combination of the above to generate insightful visualizations. 
***

### Student Bio

I am currently a Masters Student in AI at NUS. I developed a visualization dashboard using Bokeh and Python as part of GSoC 2017 for EMPA. I was a Visiting Researcher at ISI, Kolkata where I worked on predicting Cancer Survival Rates using Machine Learning Models on Molecular and Protien expression data of patients. I have industry exposure in Big Data while working for dDriven. I was responsible for creating an entire processing engine on top of Apache Spark. 
***

### Contact Information

Soumyadip Ghosh <br>
#09-595, 518 West Coast Road, Singapore - 120518 <br>
+65 94261600 <br>
gsoumyadip5@gmail.com <br>
Skype - gsoumyadip5 <br>
***

### Student Affiliation

Masters in Computing ( AI Specialization ) <br>
National University of Singapore <br>
Semester 2 <br>
***

### Schedule Conflicts
I work as a Research Assistant in the department.
***
### Mentors 

Alex Diaz-Papkovich <br>
alex.diaz-papkovich@mail.mcgill.ca <br>
Yes, I have been working with Alex regarding the selection test and the project proposal over Email and Skype. <br>
***

### Method 

#### Goal
The goal of this project is to have an interactive application in the web-browser which enables the end-user to upload genomic data files of his/her choice, clean or extract relevant information, perform dimension reduction techniques ( PCA.t-SNE,UMAP or a combination) and plot the respective graphs. Addtionally, the user must be able to save the graphs and point coordinates to the local machine along with a log file containing all the parameters of the experiment. 

#### Challenges 
1. The data can be of varied formats - VCF Files, Population panel files, TSV, CSV or FASTA Files.
2. The processing steps may be varied and numerous, combining varioud files from user input. 
3. Genomic data is typically quite large ( 100000 * 100000) or more. Thus, data processing and visualization will take significant time. 

#### Proposed Approach 

The solution would be a web application running in the browser. The solution composes of two parts 

1. A backend written in python for carrying out the necessary computation ( reading files, dimension reduction) 
2. A frontend composed of Bokeh and Datashader Elements for visualizing the data and for taking user input. 

##### Backend 

We plan to use the following open-source python libraries for this project. 

1. Bokeh
2. Scikit-Allel
3. Scikit-Learn 
4. Dask 
5. DataShader 
6. HoloViews
7. UMAP 

The proposed backend architecture comprises of three parts.

1. Data Importer Class - This class takes in the input file names and options from the front end and imports the data from the respective files. It would include  individual functions to support various file types ( VCF, CSV, TSV , Text ) and would either store the data Pandas Datafraems or in Dask Dataframes. Dask allows us to break up the data into small chunks and carry out parallel processing on it, which would be helpful, since our data is quite large. 

2. Data Processing Class - This class takes in the processing parameters from the input and the dataframes from the data Importer Class and carries out the necessary data cleaning, dimension reduction on them. (PCA, t-SNE and UMAP) would be the primary algorithms supported initially. 

3. Data Output Class - This class takes the processed data and sends it back to the front end for display. It also writes down the processed data files in a format specified from the front-end. Additionally, it also creates a log file for the entire operation. 

![Architecture Diagram](https://github.com/gmomo/genome_viz/blob/master/Architecture.png)

##### Design Choices 

We surveyed a couple of front-end plotting libraries for this project, but they all suffer from the same issue of not handling large datasets well. 

1. Chartist.js https://github.com/gionkunz/chartist-js/issues/17
2. C3.js https://github.com/c3js/c3/issues/1075
3. Google Charts - https://stackoverflow.com/questions/42972492/google-charts-large-huge-data

The only charting library which could support large datasets reliably was dybala. http://dygraphs.com/
But, unfortunately, this library has very limited charting functionalities and also little interactive feature support. It does not have a scatter plot functionality which would be a primary requirement for this project. 

Bokeh is a complete Front End Library for Data Visualizations. It has a large range of charts and very flexible customization support. It also has very good tools for user interaction. Holoviews is a library built on top of Bokeh and it interfaces very well with the DataShader Library. The Datashader library can easily render Millions of points along with supporting user interaction. Plus, it supports geographical maps which could be used as a reference background to plot the points. 

[Displaying 300 million points](http://datashader.org/index.html)
[Bokeh Interaction] (https://demo.bokeh.org/gapminder)

Scikit-Allel provides almost all the functions we need to import genetic data. It also supports parallel computation on Dask Dataframes. Scikit-Learn has an excellent implementation of t-SNE and PCA, supporting the randomized version of it as well. 






