from psp.plotting.complex_plot import ComplexPlot
from psp.plotting.plotfunc import plot_quiver
import matplotlib.pyplot as plt

class RXplot(ComplexPlot):
    """A class for creating a complex plot."""
    
    def __init__(self, title : str, figsize : tuple = (8, 8)):
        super().__init__(title, figsize = figsize)
    
    def layout(self, ax : plt.Axes):
        
        ax.set_xlim([- self._get_rmax(), self._get_rmax()])
        ax.set_ylim([- self._get_rmax(), self._get_rmax()])
        
        ax.set_xlabel(r'$R\;[\Omega]$')
        ax.set_ylabel(r'$X\;[\Omega]$')
        ax.grid(True)
        

class PolarPlot(ComplexPlot):
    """A class for creating a phasor plot using a polar projection."""
    
    def __init__(self, title : str, ax : plt.Axes = None, figsize : tuple = (8, 8)):
        super().__init__(title = title, ax = ax, figsize = figsize, projection = 'polar')
    
    def add_phasor(self, value : complex, ref : tuple = (0,0), name : str = "", color : str = None, **kwargs):
        plot_quiver(ax = self._ax,
                    phasor = value,
                    ref = ref,
                    color = color,
                    text = name,
                    polar = True,
                    alpha = 0.7,
                    **kwargs)   
        self.coordinates.append((value.real, value.imag))
    
    def layout(self, ax):
        ax.set_rlabel_position(90)
        ax.set_rlim(0, self._get_rmax())
        ax.legend()


class PhasorPlot(ComplexPlot):
    """
    A class for creating a phasor plot using a cartesian projection.
    The plot will have a centered x and y axis.
    """
    
    def __init__(self, title : str, ax : plt.Axes = None, figsize : tuple = (8, 8)):
        super().__init__(title = title, ax = ax, figsize = figsize)
    
    def layout(self, ax : plt.Axes):
        #ax.axis('equal')
        
        ax.set_xlim([- self._get_rmax(), self._get_rmax()])
        ax.set_ylim([- self._get_rmax(), self._get_rmax()])

        ax.set_aspect('equal', 'box')
   
        ax.grid(color='lightgrey', linestyle='-')
        
        
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        
        #ax = ax_dict['center']

        ax.spines[['left', 'bottom']].set_position('zero')
        ax.spines[['top', 'right']].set_visible(False)
        
        
        ax.set_xlabel('Re', fontweight='bold')
        ax.set_ylabel('Im', fontweight='bold', rotation = 0)
        
        ax.spines['left'].set_linewidth(1)
        ax.spines['left'].set_color('black')
        ax.spines['left'].set_alpha(0.8)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['bottom'].set_color('black')
        ax.spines['bottom'].set_alpha(0.8)
        
        # Remove duplicate zero in the ticks
        locs, labels = plt.yticks() # get current ticks
        locs = [n for n in locs if n != 0.0] # remove 0.0
        ax.set_yticks(locs)
        
        # Put axis label outside the plot
        ax.xaxis.set_label_coords(0.5, -0.05)
        ax.yaxis.set_label_coords(-0.05, 0.5)
        
        # Alternative to centered axis
        #ax.axhline(linewidth = 1, color ="black", linestyle ="--")
        #ax.axvline(linewidth = 1, color ="black", linestyle ="--")