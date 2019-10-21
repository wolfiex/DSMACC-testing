# d3-save-svg

 A fork of the nytimes [svg-crowbar](http://nytimes.github.io/svg-crowbar/) bookmarklet that extracts SVG nodes and accompanying styles from an HTML document and downloads them as an SVG file --- A file which you could open and edit in Adobe Illustrator, for instance. Because SVGs are resolution independent, it’s great for when you want to use web technologies to create documents that are meant to be printed (like, maybe on newsprint). It was created with [d3.js](https://d3js.org) in mind, but it should work fine no matter how you choose to generate your SVG.

[Project page](http://edeno.github.com/d3-save-svg/)

### Differences from the bookmarklet
+  Can use to download specific svg, which can be incorporated into buttons for exporting images. See example on the [project page](http://edeno.github.com/d3-save-svg/).
+  Allows specification of custom file names.
+  Handles embedded raster images.
+  Has convenience method for embedding raster images.

### Note
Most of this has been cobbled together from stackoverflow and issues logged on the nytimes svg-crowbar repo.
