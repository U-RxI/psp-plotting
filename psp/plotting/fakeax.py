from functools import partial


class FakeAx:
    """A class to collect attributes set on a plt.Axes object in order to overwrite at a later stage."""

    def __init__(self, axes):
        self.actions = []
        self.axes = axes

    def __getattr__(self, name):
        def method(*args, **kwargs):
            try:
                getattr(self.axes, name)
            except AttributeError:
                print(f"Method *{name}* do not exist in matplotlib.Axes")
                return method
            func = partial(getattr(self.axes, name), *args, **kwargs)
            self.actions.append(func)

        return method

    def overwrite(self):
        for action in self.actions:
            action()
