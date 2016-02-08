"""
Example on how to use plotter class for real time visualization
"""

from plotter import plot, subplot, series
import time
import numpy as np

size = 4
plt = plot(columns=size, name="Realtime plot");

colors = ["r","b"]

for i in range(size**2):
    sub = subplot(name="Subplot " + str(i))
    plt.add(sub)
    for j in range(2):
        seq = series(x = np.linspace(0, 100, 30), y = np.linspace(0, 100, 30), name="curve")
        seq.color = colors[j]
        sub.add(seq)

plt.compile();

idx = 100.0;

while True:
    
    for sub in plt.subplots:  
        mul = 0
        for seq in sub.sequences:              
            seq.y = (seq.y + 1) % (idx) + mul;
            mul = mul + 3;
    #idx = idx /1.1;
    time.sleep(0.01)
