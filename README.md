# PowerPoint Constructible Colors

This program aims to solve a very specific problem so watch this video from 9:58 for the explanation:
https://youtu.be/iT2pfmv3cSE?t=598

## Which Colors Are Constructible?

Currently, I have checked and found that over 99.5% of possible hex color codes are constructable, and not a single unconstructible color has been found so far.

To run the (very bad) search algorithm, run `combined.py`. It is ***highly*** recommended to use [PyPy](https://pypy.org/) for this, as otherwise it may take eons for the program to finsh (although it probably will take eons either way).

## Usage

To find a list of layers that produce a given color, use:
```python
import search
import common

target_color = (243, 17, 63) # Your RGB color

solver_result = search.solve(target_color)
if solver_result is None:
    print('Unconstructible')
else:
    print('Constructible with these layers:')
    for step in solver_result[1:]: # Exclude start node
        color = common.BASE_COLORS[step.top_layer[0]]
        opacity = common.BASE_OPACITIES[stop.top_layer[1]]
        print(opacity, color)
```
