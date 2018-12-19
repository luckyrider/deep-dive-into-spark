# WebUI Front-End Libs

## Overview
JavaScript/CSS libraries.

Static resources: 

```
core/src/main/resources/org/apache/spark/ui/static/
sql/core/src/main/resources/org/apache/spark/sql/execution/ui/static
```

| category | libs | Description |
| --- | --- | --- |
| DAG Viz | `spark-dag-viz.js` | |
|         | `spark-dag-viz.css` | |
|         | `spark-sql-viz.js` | |
|         | `spark-sql-viz.css` | |
|         | `graphlib-dot.min.js` | data structures and algorithms for parsing dot file |
|         | `dagre-d3.min.js` | dagre-d3 is a D3-based renderer for dagre |
|         | `d3.min.js` | |
| Timeline Viz | `timeline-view.js` | |
|              | `timeline-view.css` | |
|              | `vis.min.js` | vis.js is a dynamic, browser-based visualization library |
|              | `vis.min.css` | |
| | | |



## DAG Visualization

```
spark-dag-viz.js
spark-dag-viz.css
```

spark-sql-viz uses:

* `graphlib-dot.min.js`: data structures and algorithms for parsing dot file
* `dagre-d3.min.js`: dagre's focus on graph layout only. This means that you need something to actually
  render the graphs with the layout information from dagre. There are a few options for rendering:
  dagre-d3 is a D3-based renderer for dagre.
* `d3.min.js`: renderer