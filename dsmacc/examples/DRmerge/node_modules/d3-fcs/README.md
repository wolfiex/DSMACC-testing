# d3-four color scatter

Often within a scatterplot we wish to identify multiple categories, but do not want neighbouring elements to accientally end up with the same colour.



## Installing

If you use NPM, `npm install d3-fcs`. Otherwise, download the [latest release](https://github.com/wolfiex/d3-fcs

## API Reference

Refer to the observable notebook (@wolfiex), or test file (in the test directory on the github repository)

https://observablehq.com/@wolfiex/d3-fcs-demo


```
fcs = require('d3-fcs')

// create an array of x,y,category for all points in the plot

var scatter = data.map(n=>{return {x:...,y:...,c:...}})

var cdict = fcs.ccat(scatter)


// plot
svg.append('circle')
    ...
    .fill(d=>cdict[d.c])

```
