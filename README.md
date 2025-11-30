# PowerPoint Constructible Colors

This program aims to solve a very specific problem so watch this video from 9:58 for the explanation:
https://youtu.be/iT2pfmv3cSE?t=598

## Requirements

Use `pip install -r requirements.txt` to get everything you need.

## Which Colors Are Constructible?

Currently, I have checked and found that over 99.67% of possible hex color codes are constructible, and not a single unconstructible color has been found so far. It is very likely that every color is constructible, I just don't know how to prove it.

To run the (very bad) search algorithm, run `combined.py`. It is ***highly*** recommended to use [PyPy](https://pypy.org/) for this, as otherwise it may take eons for the program to finsh (although it probably will take eons either way). The searcher will passively consume 1-2 GiB of RAM, and the `constructible_colors.dat` file it will produce can be up to 50 MiB.

While the search algorithm is running or after it stops, run `check_remaining_colors.py` to see a sample of colors that haven't been proven constructible yet.

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
