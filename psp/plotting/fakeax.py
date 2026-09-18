from functools import partial


class _AttributeProxy:
    """Records an attribute/item path originating from a FakeAx."""

    def __init__(self, fake_ax, path):
        # Use object.__setattr__ to avoid triggering our own __setattr__ logic.
        object.__setattr__(self, "_fake_ax", fake_ax)
        object.__setattr__(self, "_path", path)

    def __getattr__(self, name):
        """Add an attribute lookup to the recorded path."""
        return _AttributeProxy(
            self._fake_ax,
            self._path + [("attr", name)],
        )

    def __getitem__(self, key):
        """Add an item lookup, such as spines['left'], to the path."""
        return _AttributeProxy(
            self._fake_ax,
            self._path + [("item", key)],
        )

    def __call__(self, *args, **kwargs):
        """Record a method call at the end of the path."""
        self._fake_ax._validate_call(self._path, args, kwargs)
        self._fake_ax.historic.append((self._path, args, kwargs))

        # Returning self allows some chained call patterns to be represented.
        return self


class FakeAx:
    """
    Collect method calls made on a matplotlib Axes object and replay
    them later on the original axes or another axes.
    """

    def __init__(self, axes):
        self.axes = axes
        self.historic = []

    def __getattr__(self, name):
        """
        Begin recording a path from the underlying Axes object.

        Examples:
            fake_ax.set_xlim(0, 10)
            fake_ax.spines["left"].set_position("zero")
            fake_ax.xaxis.set_visible(False)
        """
        return _AttributeProxy(
            self,
            [("attr", name)],
        )

    @staticmethod
    def _resolve_path(root, path):
        """Resolve an attribute/item path against a real object."""
        obj = root

        for operation, value in path:
            if operation == "attr":
                obj = getattr(obj, value)
            elif operation == "item":
                obj = obj[value]
            else:
                raise ValueError(f"Unknown path operation: {operation!r}")

        return obj

    def _validate_call(self, path, args, kwargs):
        """
        Validate the recorded call against the template Axes object.

        This checks that the path exists and ends in something callable,
        but does not execute the method.
        """
        try:
            method = self._resolve_path(self.axes, path)
        except (AttributeError, KeyError, IndexError, TypeError) as exc:
            formatted_path = self._format_path(path)
            raise AttributeError(
                f"{formatted_path} does not exist on the supplied Axes object"
            ) from exc

        if not callable(method):
            formatted_path = self._format_path(path)
            raise TypeError(f"{formatted_path} exists, but it is not callable")

    @staticmethod
    def _format_path(path):
        """Create a readable representation of a recorded path."""
        result = "ax"

        for operation, value in path:
            if operation == "attr":
                result += f".{value}"
            elif operation == "item":
                result += f"[{value!r}]"

        return result

    def _replay(self, ax):
        """Replay all recorded calls on a supplied Axes object."""
        for path, args, kwargs in self.historic:
            method = self._resolve_path(ax, path)

            if not callable(method):
                formatted_path = self._format_path(path)
                raise TypeError(f"{formatted_path} is not callable on the target Axes")

            method(*args, **kwargs)

    def overwrite(self):
        """Replay the recorded calls on the original Axes object."""
        self._replay(self.axes)

    def copy(self, ax):
        """Replay the recorded calls on another Axes object."""
        self._replay(ax)

    def clear(self):
        """Remove all recorded calls."""
        self.historic.clear()


# class FakeAx:
# """A class to collect attributes set on a plt.Axes object in order to overwrite at a later stage."""

# def __init__(self, axes):
# self.actions = []
# self.historic = []
# self.axes = axes

# def __getattr__(self, name):
# def method(*args, **kwargs):
# try:
# getattr(self.axes, name)
# except AttributeError:
# print(f"Method *{name}* do not exist in matplotlib.Axes")
# return method
# func = partial(getattr(self.axes, name), *args, **kwargs)
# self.actions.append(func)
# self.historic.append((name, args, kwargs))

# return method

# def overwrite(self):
# for action in self.actions:
# action()

# def copy(self, ax):
# for name, args, kwargs in self.historic:
# func = getattr(ax, name)
# func(*args, **kwargs)
