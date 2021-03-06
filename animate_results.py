

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation


class animate():
    def __init__(self, x, y, z, times):
        """
        array is 2d with time on axis=0 and function values for x
        points on axis=1
        """
        # setup data
        self.x = x
        self.y = y
        self.z = z
        self.times = times
        self.N = len(times)
        assert self.N == len(x) == len(y) == len(z), \
            'all inputs need same number of time entries'
#        assert x.shape[1] == y.shape[1] == z.shape[1], \
#            'all inputs need same number of points enteries'

        # setup options
        self.save = ''
        self.interval = 20
        x_max, x_min = max(self.x[0]), min(self.x[0])
        y_max, y_min = max(self.y[0]), min(self.y[0])
        r_x = x_max - x_min
        r_y = y_max - y_min
        self.xlims = np.array([x_min - r_x/10, x_max + r_x/10])
        self.ylims = np.array([y_min - r_y/10, y_max + r_y/10])
        self.fig = None
        
        # find the color range
        z_min = min([min(z_) for z_ in z])
        z_max = max([max(z_) for z_ in z])
        self.z_lims = [z_min, z_max]
        
    def blank(self):
        self.scat = self.ax.scatter([], [])
        self.text.set_text('')
        return self.scat, self.text

    def update(self, i):
        self.scat = self.ax.scatter(self.x[i], self.y[i], s=20, c=self.z[i],
                                    vmin=self.z_lims[0], vmax=self.z_lims[1])
        self.text.set_text('t={0:.2f}'.format(self.times[i]))
        return self.scat, self.text

    def set_figure(self, title='', color_key=''):
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter([], [], c=[],
                                    vmin=self.z_lims[0], vmax=self.z_lims[1])
        self.col = self.fig.colorbar(self.scat)
        self.col.set_label(color_key)
        self.text = self.ax.text(0.75, 0.95, '', transform=self.ax.transAxes)

        # set axis limits
        self.ax.set_xlim(self.xlims)
        self.ax.set_ylim(self.ylims)
        self.ax.set(title=title, xlabel='X [m]', ylabel='Y [m]')

    def animate(self, ani_step=1):
        """
        Animates a class object creared by load_and_set() function

        Parameters
        ---------
        ani_step: int
            frame skipping
        """
        assert self.fig is not None, 'must run set_figure first'
        # animate
        self.ani = FuncAnimation(self.fig,
                                 self.update,frames=range(0, len(self.times), ani_step),
                                 interval=self.interval,
                                 blit=True,
                                 init_func=self.blank)
        if self.save != "":
            self.ani.save(self.save)


def load_and_set(file_name, ani_key='V_x'):
    """
    Function to load a file and set animation class instances. To run animation
    call animate() method on returned object.

    Parameters
    ----------
    file_name: string
        name of the file to load. Should be generated by sph_simulate()
    ani_key: string
        header for colorplot. Choose beteween: ID, Pressure, Density, V_x, and V_y

    Returns
    -------
    ani: class object
        From the instance of animate
    """
    # load data
    data = pd.read_csv(file_name, skiprows=2, index_col=False)
    data = data.set_index('Time')
    # format data
    times = np.unique(data.index)
    x, y, z = [], [], []
    for t in times:
        x.append(data.loc[t]['R_x'])
        y.append(data.loc[t]['R_y'])
        z.append(data.loc[t][ani_key])
    # run animation
    ani = animate(x, y, z, times)
    ani.set_figure(color_key=ani_key)
    return ani


if __name__ == '__main__':

    ani = load_and_set('./raw_data/example3.csv', 'Density')
    # ani = load_and_set(domain.file.name, 'Density')
    ani.animate(ani_step=20)
    plt.show()
