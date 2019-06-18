## Fractal Explorer
*****

### Julia Sets

This script generates a Tkinter GUI to preview and render [Julia set](http://mathworld.wolfram.com/JuliaSet.html) fractals. Quadratic Julia sets are generated by the expression
<img src="/tex/960774e1cabda84cf25239113699a14d.svg?invert_in_darkmode&sanitize=true" align=middle width=98.95171934999999pt height=26.76175259999998pt/>
where _c_ is a constant.

Sets whose value of _c_ lies within the [Mandlebrot set](http://mathworld.wolfram.com/MandelbrotSet.html) remain connected and are called Fatou sets, and other values of _c_ form disconnected, interesting fractal patterns called Cantor sets or Fatou dust.

### Changes

This was my first attempt at creating a packaged GUI for any of my projects, and it made me realize how slow creating a desktop executable is. Additionally, the fractal rendering system currently uses nested for-loops to generate the fractal, which is slow and resistant to changes in window size or zoom. Finding a way to utilize iterative vectorized functions and filter() would dramatically reduce the rendering time which would allow for a dynamic window size or zoom level.

Additionally I'd like to add
