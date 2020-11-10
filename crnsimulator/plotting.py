
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid", font_scale=1, rc={"lines.linewidth": 2.0})

def ode_plotter(name, t, ny, svars, log = False, labels = None,
        xlim = None, ylim = None, plim = None, labels_strict = False):
    """ Plots the ODE trajectories.

    Args:
      name (str): Name of the outputfile including extension (e.g. *.pdf)
      t (list[flt]) : time units plotted on the x-axis.
      ny (list[list[flt]]) : a list of trajectories plotted on the y-axis.
      svars (list[str]): A list of names for every trajectory in ny
      log (bool,optional): Plot data on a logarithmic time scale
      labels (set(),optional): Define species that appear labelled in the plot
      xlim ((float,float), optional): matplotlib xlim.
      ylim ((float,float), optional): matplotlib ylim.
      plim (float, optional): Minimal occupancy to plot a trajectory. Defaults to None.
      labels_strict (bool, optional): Only print labels that were specified using labels.

    Prints:
      A file containing the plot (Format *.pdf, *.png, etc.)

    Returns:
      [str]: Name of the file containing the plot
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 4.5))

    # b : blue.
    # g : green.
    # r : red.
    # c : cyan.
    # m : magenta.
    # y : yellow.
    # k : black.
    mycolors = ['blue', 
                'red', 
                'green', 
                'orange', 
                'maroon', 
                'springgreen', 
                'cyan', 
                'magenta', 
                'yellow']
    mycolors += list('kkkkkkkkkkk')

    if labels:
        i = 0
        for e, y in enumerate(ny):
            if svars[e] in labels:
                ax.plot(t, y, '-', label=svars[e], color=mycolors[i])
                i = i + 1 if i < len(mycolors) - 1 else 0
            elif not labels_strict:
                ax.plot(t, y, '--', lw=0.1, color='gray', zorder=1)
    else:
        for e, y in enumerate(ny):
            if plim is None or max(y) > plim:
                ax.plot(t, y, '-', label=svars[e])
            else:
                ax.plot(t, y, '--', lw=0.1, color='gray', zorder=1)

    plt.title(name)
    if xlim:
        plt.xlim(xlim)
    # plt.xticks(np.arange(0, 61, step=20))

    if ylim:
        plt.ylim(ylim)
    # plt.yticks(np.arange(0, 51, step=10))

    ax.set_xlabel('Time', fontsize=16)
    ax.set_ylabel('Concentration', fontsize=16)
    if log:
        ax.set_xscale('log')
    else:
        ax.set_xscale('linear')

    plt.legend(loc='upper right')
    fig.tight_layout()
    plt.savefig(name)
    plt.close()
    return name

