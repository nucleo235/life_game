import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib import animation

class Life:
    """A Game of Life simulator."""

    def __init__(self, arr, pad=25, contamination=False):
        """Initialize the instance.

        The provided array consists of zero and non-zero entries,
        representing dead and alive cells, respectively. It is optionally
        padded by width pad on all sides with zeros.

        """

        # Set the "world" array as boolean and initialize the figure.
        # The world is depicted as a black-and-white array of squares.
        self.arr = arr.astype(bool)
        self.arr = np.pad(self.arr, pad)
        self.contamination = contamination
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.arr, cmap=plt.cm.binary,
                                 interpolation='nearest')
        self.label = self.ax.text(0, 0, '', ha='left', va='bottom', fontsize=10, color="Red")
        # Remove the Axes tick marks.
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def do_step(self):
        """Advance the Game of Life world by one generation."""

        # Use convolution method to count neighbours, e.g.
        # http://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
        boost = 3
        nn = convolve2d(self.arr, np.ones((boost, boost)), mode='same',
                        boundary='wrap') - self.arr
        self.arr = (nn == boost) | (self.arr & (nn == boost-1))
        
        # a bit of randomness in life
        if self.contamination:
            x = True
            deathx = np.random.randint(0, len(self.arr))
            deathy = np.random.randint(0, len(self.arr))
            self.arr[deathx,deathy] = x
            self.arr[deathx-1,deathy] = x
            self.arr[deathx-1,deathy-1] = x
            self.arr[deathx,deathy-1] = x
            self.arr[deathx,deathy-2] = x
            self.arr[deathx-1,deathy-2] = x

    def init_animation(self):
        """Initialize the animation: self.im is updated on each time step."""

        self.im.set_data(np.zeros_like(self.arr))
        return self.im,

    def animate(self, i):
        """Draw the current state of the world and advance by one time step."""
        
        self.im.set_data(self.arr)
        self.do_step()
        self.label.set_text('cells: %.3f' %(np.sum(self.arr)/len(arr)**2) )
        

    def play(self, frames=10000, interval=0.1):
        """Play the Game of Life, depicted as a Matplotlib animation."""

        anim = animation.FuncAnimation(self.fig, self.animate,
                    init_func=self.init_animation, frames=frames,
                    interval=interval)
        # If we're saving the animation as a video, uncomment these two lines.
        #writer = animation.FFMpegWriter(fps=4)
        #anim.save('life.mp4', writer=writer)

        # If we're just viewing the animation locally, uncomment this line.
        plt.show()

def randomGrid( N):

    """returns a grid of NxN random values"""
    return np.random.choice([0,1], N*N, p=[0.9, 0.1]).reshape(N, N)

if __name__ == "__main__":

    N = 2**8
    arr = randomGrid(N) #np.random.randint(0,1, size=(64,1))
    life = Life(arr, pad=0, contamination=False)
    life.play()