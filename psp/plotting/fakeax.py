class FakeAx:
    def __init__(self, axes):
        self.actions = []
        self.axes = axes
        
    def __getattr__(self, name):
        def method(*args, **kwargs):
            try:
                getattr(self.axes, name)
            except:
                print(f'Method *{name}* do not exist in matplotlib.Axes')
                return method
            func = partial(getattr(self.axes, name), *args, **kwargs)
            self.actions.append(func)
        return method
    
    def overwrite(self):
        for action in self.actions:
            action()