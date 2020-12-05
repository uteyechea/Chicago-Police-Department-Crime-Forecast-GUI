#!/usr/bin/env python
# coding: utf-8

# In[21]:


import numpy as np


# In[22]:


def beat_polygon_vertex(beat_tally=303,beat_grid_vertex=None):
    
    #Number of beats inside the square grid selected previously
    number_of_beats_per_side=int(np.around(np.sqrt(beat_tally),0))
    
    height=abs(beat_grid_vertex['top'][0][0]-beat_grid_vertex['bottom'][0][0])
    width=abs(beat_grid_vertex['top'][0][1]-beat_grid_vertex['top'][1][1])
    delta_longitude=width/number_of_beats_per_side
    delta_latitude=height/number_of_beats_per_side
    
    #Grid starting coordinates (Top left vertex, assuming a square)
    latitude=beat_grid_vertex['top'][0][0]
    longitude=beat_grid_vertex['top'][0][1]

    beat={}
    for n in range(number_of_beats_per_side+1):
        for m in range(number_of_beats_per_side):
            top_left=[latitude-(n*delta_latitude),longitude+(m*delta_longitude)]
            top_right=[latitude-(n*delta_latitude),longitude+((m+1)*delta_longitude)]
            bottom_left=[latitude-((n+1)*delta_latitude),longitude+(m*delta_longitude)]
            bottom_right=[latitude-((n+1)*delta_latitude),longitude+((m+1)*delta_longitude)]
    
            beat[number_of_beats_per_side*n+m]=[top_left, top_right, bottom_right, bottom_left]
        
    return beat 

    
# In[24]:


#Usage example
"""
#Record vertex of square on top of city of interest
beat_grid_vertex={'top':[[29.1540,-111.0070],[29.1540,-110.9400]],
                  'bottom':[[29.0080,-111.0070],[29.0080,-110.9400]]
                  }

#Map coordinates per beat
beat=beat_polygon_vertex(beat_grid_vertex=beat_grid_vertex)
print(beat)

"""


# In[ ]:




