# psp-plotting

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

psp-plotting is a Python library for creating power system protection plots using matplotlib.


## Disclaimer
**This package is currently under active development and may undergo significant changes. Features may be incomplete, unstable, or subject to breaking modifications without notice.**

## Installation

Use the package manager uv[uv](https://docs.astral.sh/uv/) to install pspplot.

```bash
uv pip install "git+https://github.com/U-RxI/psp-plot"
```

## Usage

```python
from psp.plotting import RXplot

myplot = RXplot('RX plot with phasors')
myplot.add_phasor(value=1+0j, color='Red', name='U1')
myplot.add_phasor(value=-0.5-0.866j, color='Blue', name='U2')
myplot.add_phasor(value=-0.5+0.866j, color='Green', name='U3')
myplot.show()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)