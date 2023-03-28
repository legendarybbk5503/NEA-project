import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy
from sklearn.linear_model import LinearRegression
from random import randint

reg = LinearRegression()

x_values = []
y_values = []

for i in range(1000):
    plt.clf()
    
    x_values.append(randint(0, 100))
    y_values.append(randint(0, 100))

    x = numpy.array(x_values)
    y = numpy.array(y_values)
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    if i % 20 == 0:
        reg.fit(x, y)
        plt.gca().set_aspect('equal')
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.scatter(x_values, y_values, color = 'black')
        plt.plot(
            list(range(100)),
            reg.predict(numpy.array(list(range(100))).reshape(-1, 1)),
        )
        plt.pause(0.01)

plt.show()
