from sklearn import datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = ['sub', 'pub_f', 'au_f', 'dew_f', 'dew_id', 'pub_id', 'num_pg', 'pubp_id', 'au_id', 'pubp_f', 'ti_avg', 'ti_num', 'subp']
y = [0.302861, 0.209978, 0.183955, 0.093093, 0.049930, 0.048432, 0.038660, 0.017514, 0.016030, 0.011857, 0.010435, 0.010353, 0.006902]

plt.bar(x, y, align='center', alpha=0.5)
#plt.xticks(y_pos, objects)
plt.0title('RF- Importance of Each Feature')
plt.xlabel('Feature')
plt.ylabel('Strength')
plt.show()
