import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

uniform_data = np.random.rand(10, 12);
print uniform_data;
ax = sns.heatmap(uniform_data);
plt.show();
