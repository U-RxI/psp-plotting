from psp.plotting.complex_plot import ComplexPlot
from psp.plotting.plotfunc import plot_quiver
import matplotlib.pyplot as plt

class RXplot(ComplexPlot):
    """A class for creating a complex plot."""
    
    def __init__(self, title : str, figsize : tuple = (8, 8)):
        super().__init__(title, figsize = figsize)
    
    def layout(self, axes : plt.Axes):
        
        axes.set_xlim([- self._get_rmax(), self._get_rmax()])
        axes.set_ylim([- self._get_rmax(), self._get_rmax()])
        
        axes.set_xlabel(r'$R\;[\Omega]$')
        axes.set_ylabel(r'$X\;[\Omega]$')
        axes.grid(True)
        

class PolarPlot(ComplexPlot):
    """A class for creating a phasor plot using a polar projection."""
    
    def __init__(self, title : str, axes : plt.Axes = None, figsize : tuple = (8, 8)):
        super().__init__(title = title, axes = axes, figsize = figsize, projection = 'polar')
    
    def add_phasor(self, value : complex, ref : tuple = (0,0), name : str = "", color : str = None, **kwargs):
        plot_quiver(axes = self._axes,
                    phasor = value,
                    ref = ref,
                    color = color,
                    text = name,
                    polar = True,
                    alpha = 0.7,
                    **kwargs)   
        self.coordinates.append((value.real, value.imag))
    
    def layout(self, axes):
        axes.set_rlabel_position(90) 
        axes.set_rlim(0, self._get_rmax())
        axes.legend()


class PhasorPlot(ComplexPlot):
    """
    A class for creating a phasor plot using a cartesian projection.
    The plot will have a centered x and y axis.
    """
    
    def __init__(self, title : str, axes : plt.Axes = None, figsize : tuple = (8, 8)):
        super().__init__(title = title, axes = axes, figsize = figsize)
    
    def layout(self, axes : plt.Axes):
        #axes.axis('equal')
        
        axes.set_xlim([- self._get_rmax(), self._get_rmax()])
        axes.set_ylim([- self._get_rmax(), self._get_rmax()])

        axes.set_aspect('equal', 'box')
   
        axes.grid(color='lightgrey', linestyle='-')
        
        
        axes.spines['left'].set_position('zero')
        axes.spines['bottom'].set_position('zero')
        
        #ax = ax_dict['center']

        axes.spines[['left', 'bottom']].set_position('zero')
        axes.spines[['top', 'right']].set_visible(False)
        
        
        axes.set_xlabel('Re', fontweight='bold')
        axes.set_ylabel('Im', fontweight='bold', rotation = 0)
        
        axes.spines['left'].set_linewidth(1)
        axes.spines['left'].set_color('black')
        axes.spines['left'].set_alpha(0.8)
        axes.spines['bottom'].set_linewidth(1)
        axes.spines['bottom'].set_color('black')
        axes.spines['bottom'].set_alpha(0.8)
        
        # Remove duplicate zero in the ticks
        locs, labels = plt.yticks() # get current ticks
        locs = [n for n in locs if n != 0.0] # remove 0.0
        axes.set_yticks(locs)
        
        # Put axis label outside the plot
        axes.xaxis.set_label_coords(0.5, -0.05)
        axes.yaxis.set_label_coords(-0.05, 0.5)
        
        # Alternative to centered axis
        #axes.axhline(linewidth = 1, color ="black", linestyle ="--")
        #axes.axvline(linewidth = 1, color ="black", linestyle ="--")