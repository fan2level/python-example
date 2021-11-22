import matplotlib .pyplot as plt
import squarify

plt.style.use('default')
plt.rcParams['figure.figsize'] = (4,4)
plt.rcParams['font.size'] = 12

sizes = [40, 30, 5, 25]
labels = ['A', 'B', 'C', 'D']
colors = ['lightgreen', 'cornflowerblue', 'mediumpurple', 'lightcoral']

squarify.plot(sizes, 10, 10, label=labels, color=colors)

plt.axis('off')
plt.show()
