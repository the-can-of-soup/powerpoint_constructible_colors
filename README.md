# PowerPoint Constructible Colors

This program aims to solve a very specific problem so watch this video from 9:58 for the explanation:
https://youtu.be/iT2pfmv3cSE?t=598

## Rounding

This project currently assumes the following layer overlay behavior:

Given a bottom color `B`, a layer color `L`, and a layer opacity `α`, the formula used for the result color `C` is:
```
C = round(B + α * (L - B))
```

However, this is not exactly how PowerPoint performs layering from what I can tell. I do not know the formula that PowerPoint uses, so this project just uses the above formula, which is usually a very close approximation.

## Requirements

Use `pip install -r requirements.txt` to get everything you need to use the program.

## Which Colors Are Constructible?

Currently, I have checked and found that at least 99.91% of possible hex color codes are constructible, and not a single unconstructible color has been found so far. It is very likely that every color is constructible, I just don't know how to prove it.

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
