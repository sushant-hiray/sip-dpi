import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt

def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", cmap=cm.gist_rainbow):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",stacked=True, ax = axe, colormap=cmap, legend=False)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0,n_df*n_col,n_col): # len(h) = n_col * n_df
        for j,pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x()+1/float(n_df+1)*i/n_col)
                rect.set_hatch(H*(i/n_col))
                rect.set_width(1/float(n_df+1))

    plt.xticks((np.arange(1,2*n_ind,2)+1/float(n_df+1))/2., df1.index, rotation = 0)        
    plt.title(title)
    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0,0,color = "gray", hatch=H*i))

    l1 = plt.legend(h[:n_col],l[:n_col],loc=[1.01,0.5])
    if labels is not None:
        l2 = plt.legend(n,labels,loc=[1.01,0.1]) 
    plt.gca().add_artist(l1)
    return axe


# create fake dataframes
df1 = pd.DataFrame(np.random.rand(4,5),index=["A","B","C","D"],columns=["I","J","K","L","M"])
# df2 = pd.DataFrame(np.random.rand(4,5),index=["A","B","C","D"],columns=["I","J","K","L","M"])
# df3 = pd.DataFrame(np.random.rand(4,5),index=["A","B","C","D"],columns=["I","J","K","L","M"])

# Then, just call :
plot_clustered_stacked([df1],["df1"])