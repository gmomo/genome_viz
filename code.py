#Required Imports
import allel
import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import PCA
import umap
import matplotlib.pyplot as plt
import seaborn as sns
import time 

'''
Main Class GenomzeViz
load_data() -> loads data from the three files specified
run() -> ouputs the log,coordinates and plot files. Takes n_samples as optional argument
The unique file names are named by timestamp 
'''
class GenomeViz:
    def __init__(self):
        self.genome_file = None
        self.panel_file = None
        self.population_file = None
        self.timestamp = int(time.time())
        self.seed = 42
        np.random.seed(42) #Set Random Seed

    def load_data(self,genome_file,panel_file,population_file): 
    	'''
    	Load files and create the population codes and description files
    	'''
        self.genome_file = allel.read_vcf(genome_file)
        self.panel_file = pd.read_csv(panel_file, sep='\t')
        self.population_file = pd.read_csv(population_file, sep="\t")
        
        #Basic Processing
        self.panel_file['pop'] = self.panel_file['pop'].str.strip()
        self.panel_pop = self.panel_file['pop'].values
        self.df_code = self.population_file["Population Code"].dropna().values
        self.df_desc = self.population_file["Population Description"].dropna().values[:-1]
        
    def run(self,n_samples=1000):
    	'''
    	Run PCA and UMAP on the data. 
    	'''
        start = time.time()
        self.timestamp = int(start)
        
        gt = allel.GenotypeChunkedArray(self.genome_file['calldata/GT'])
        gn = gt.to_n_alt()
        vidx = np.random.choice(gn.shape[0], n_samples, replace=False)
        vidx.sort()
        gnr = gn.take(vidx, axis=0)[:]
            
        pca = PCA(n_components=2)
        gnu_pca = pca.fit_transform(gnr.T)
        
        reducer = umap.UMAP()
        #gnu_umap = reducer.fit_transform(gnr.T)
        
        gnu_pca_df = pd.DataFrame(gnu_pca,self.panel_pop)
        gnu_pca_df["pop"] = gnu_pca_df.index
        
        gnu_umap_df = pd.DataFrame(gnu_pca,self.panel_pop)
        gnu_umap_df["pop"] = gnu_umap_df.index
        
        plot_signal = self.plot(gnu_pca_df,gnu_umap_df)
        write_signal = self.write(gnu_pca_df,gnu_umap_df)
        
        end = time.time()
        
        if(plot_signal and write_signal):
            log_file = open(str(self.timestamp) + ".log","w+")
            log_file.write("Log File Start \n")
            log_file.write("\nRun time : " + str(end - start))
            
            log_file.write("\nRandom Seed : " + str(self.seed))
            
            log_file.write("\nPackage Versions : \n")
            log_file.write("\nScikit Allel Version : " + str(allel.__version__))
            log_file.write("\nSklearn Version : " + str(sklearn.__version__))
            log_file.write("\nNumpy Version : " + str(np.__version__))
            #log_file.write("Matplotlib Version : " + str(matplotlib.__version__))
            log_file.write("\nPandas Version : " + str(pd.__version__))
            log_file.write("\nUMAP Version : " + str(umap.__version__))
            
            log_file.write("\nPCA Parameters : \n")
            log_file.write(str(pca))
            log_file.write("\nUMAP Parameters : \n")
            log_file.write(str(reducer))
            
            log_file.close()
            
    def plot(self,gnu_pca_df,gnu_umap_df):
        sns.set(style='white', context='notebook', rc={'figure.figsize':(14,10)})
        code_colour = sns.color_palette("husl", len(self.df_code))
        
        g = sns.scatterplot(x=0,y=1,hue="pop",hue_order = self.df_code,data=gnu_pca_df,palette=code_colour,legend=False)
        g.set_ylabel("Y1")
        g.set_xlabel("X1")
        g.set_title("PCA Plot")

        custom = []
        for colours in code_colour:    
            custom.append(Line2D([], [], marker='s', color=colours, linestyle='None'))
        lgd = plt.legend(custom,self.df_desc, loc='center left', bbox_to_anchor=(1, 0.5),title="Population Categories")

        fig = g.get_figure()
        fig.savefig(str(self.timestamp) + ".png",bbox_extra_artists=(lgd,), bbox_inches='tight')
        
        return 1
    
    def write(self,gnu_pca_df,gnu_umap_df):
        try:
            with open(str(self.timestamp) + '.txt', 'w') as f:
                f.write("PCA Coordinates\n")
                f.write(gnu_pca_df.to_string())
                f.write("\n UMAP Coordinates \n")
                f.write(gnu_umap_df.to_string())
            return 1
        except:
            return 0    
        

gviz = GenomeViz()
gviz.load_data("ALL.wgs.nhgri_coriell_affy_6.20140825.genotypes_has_ped.vcf","affy_samples.20141118.panel","20131219.populations.tsv")

gviz.run()
