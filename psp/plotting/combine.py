class CombineFigure():
    
    def __init__(self, nrows : int, ncols : int, figsize : tuple = (8, 8)):
        """
        Constructs all the necessary attributes for the CombineFigure object.

        Parameters
        ----------
        nrows : int
            Number of rows.
        ncols : int
            Number of columns.
        figsize : tuple, optional
            Figure size of the matplotlib.pylot figure. The default is (8, 8).

        Returns
        -------
        None.

        """
        self.nrows = nrows
        self.ncols = ncols
        self.figsize = figsize
        self.fig = plt.figure(figsize=self.figsize, layout="constrained")
        self.axes = []
        self.i = 0
        
    def add_axis(self, projection = None):
        self.i += 1
        ax = self.fig.add_subplot(self.nrows, self.ncols, self.i, projection=projection)
        self.axes.append(ax)
        return ax
        
    def _maximize_window(self):
        """
        Method to maximize the figure. 

        Returns
        -------
        None.

        """
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    
    def show(self, maximize : bool = False):
        """
        Method to show the stored plot.

        Parameters
        ----------
        maximize : bool, optional
            Option to maximize the plot window. The default is False.

        Returns
        -------
        None.

        """
        if maximize:
            self._maximize_window()
        plt.show()