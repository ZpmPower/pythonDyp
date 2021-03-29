# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def drawCategoryCountPlot(categories,cat_count):
    fig, ax = plt.subplots(figsize =(16, 9))
    ax.barh(categories, cat_count)
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
    # Show top values
    ax.invert_yaxis()
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
    # Add Plot Title
    ax.set_title('Сategoty Count',loc ='left', )
    # Add Text watermark
    fig.text(0.9, 0.15, 'bohdan_sydorov', fontsize = 12,
                 color ='grey', ha ='right', va ='bottom',
                 alpha = 0.7)
        # Show Plot
    plt.show()