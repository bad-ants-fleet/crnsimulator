
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def ode_plotter(name, t, ny, svars, lin_time, log_time, labels = None,
        plim = None, labels_strict = False):
    """ Plots the ODE trajectories.

    Args:
      name (str): Name of the outputfile including extension (e.g. *.pdf)
      t (list[flt]) : time units plotted on the x-axis.
      ny (list[list[flt]]) : a list of trajectories plotted on the y-axis.
      svars (list[str]): A list of names for every trajectory in ny
      lin_time: 
      log_time: 
      labels (set(),optional): Define species that appear labelled in the plot
      plim (float, optional): Minimal occupancy to plot a trajectory. Defaults to None.
      labels_strict (bool, optional): Only print labels that were specified using labels.

    Prints:
      A file containing the plot (Format *.pdf, *.png, etc.)

    Returns:
      [str]: Name of the file containing the plot
    """
    fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 10]})
    fig.set_size_inches(7, 3)
    plt.subplots_adjust(wspace=0)

    [ax1, ax2] = axs
    ax1.set_xscale('linear')
    ax1.spines['right'].set_visible(False)
    ax1.set_xlim((0, lin_time))
    #ax1.set_ylim([-0.02, 1.02])
    # Tick business
    ax1.set_xticks([0])

    ax2.set_xscale('log')
    ax2.spines['left'].set_visible(False)
    ax2.set_xlim((lin_time, log_time))
    #ax2.set_ylim([-0.02, 1.02])
    # Tick business
    ax2.yaxis.tick_right()
    ax2.set_yticklabels([])

    # TODO: hmmmm
    ax2.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))
    #ax2.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, numticks=10))
    #ax2.xaxis.set_minor_formatter(ticker.FormatStrFormatter("%.2f"))

    # Mark the end of transcription.
    ax1.axvline(x = lin_time, linewidth = 1, color = 'black', linestyle = '-') 
    ax2.axvline(x = lin_time, linewidth = 1, color = 'black', linestyle = '-') 

    # Set the grid lines.
    ax1.grid(axis = 'y', which = 'major', alpha = 0.7,
             color='gray', linestyle='--', linewidth=0.5)
    ax2.grid(axis = 'y', which = 'major', alpha = 0.7, 
             color='gray', linestyle='--', linewidth=0.5)
    ax1.grid(axis = 'x', which = 'major', alpha = 0.7,
             color='gray', linestyle='--', linewidth=0.5)
    ax2.grid(axis = 'x', which = 'major', alpha = 0.7, 
             color='gray', linestyle='--', linewidth=0.5)

    mycolors = ['blue', 'red', 'green', 'orange', 'maroon', 
                'springgreen', 'cyan', 'magenta', 'yellow']
    mycolors += ['k' for _ in range(len(ny))] # rest is black.
 
    if labels:
        i = 0
        for e, y in enumerate(ny):
            if svars[e] in labels:
                p, = ax1.plot(t, y, '-', color = mycolors[i], lw=1.5)
                l, = ax2.plot(t, y, '-', color = mycolors[i], lw=1.5, label = svars[e])
                i += 1
            elif not labels_strict:
                p, = ax1.plot(t, y, '-', color = 'gray', lw=0.1, zorder = 1)
                l, = ax2.plot(t, y, '-', color = 'gray', lw=0.1, zorder = 1)
    else:
        for e, y in enumerate(ny):
            if plim is None or max(y) > plim:
                p, = ax1.plot(t, y, '-')
                l, = ax2.plot(t, y, '-', label = svars[e])
            else:
                p, = ax1.plot(t, y, '--', lw = 0.1, color='gray', zorder = 1)
                l, = ax2.plot(t, y, '--', lw = 0.1, color='gray', zorder = 1)

    # Legends and labels.
    ax1.set_ylabel('occupancy')
    ax2.set_xlabel('time (seconds)')
    ax1.xaxis.set_label_coords(0.7, -0.15)
    ax2.legend()
    ax2.legend(ncol=1, loc = "center right", frameon = True, facecolor = 'white', framealpha = 0.8)

    # Save a file.
    plt.savefig(name, bbox_inches = 'tight')
    return

