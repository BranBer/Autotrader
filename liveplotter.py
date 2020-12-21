import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import count
import pandas as pd
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')

x_vals = []
y_vals = []

index = count()

fig1 = None
fig2 = None
fig3 = None

def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    #plt.xlim(left = len(x_vals) - 10, right = len(x_vals))
    fig1 = plt.figure()
    plt.cla()
    plt.plot(x_vals[-100:], y_vals[-100:])
    plt.tight_layout()
    
def animate2(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    #plt.xlim(left = len(x_vals) - 10, right = len(x_vals))
    fig2 = plt.figure()
    plt.cla()
    plt.plot(x_vals[-100:], y_vals[-100:])
    plt.tight_layout()

def animate2(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    #plt.xlim(left = len(x_vals) - 10, right = len(x_vals))
    fig3 = plt.figure()
    plt.cla()
    plt.plot(x_vals[-100:], y_vals[-100:])
    plt.tight_layout()

ani = FuncAnimation(fig1, animate, frames = 10, interval=1, save_count=5)
ani = FuncAnimation(fig2, animate, frames = 10, interval=1, save_count=5)
ani = FuncAnimation(fig3, animate, frames = 10, interval=1, save_count=5)

plt.show()
