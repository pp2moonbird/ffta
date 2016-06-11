# 6/11
## [d3 selector](https://github.com/d3/d3/wiki/Selections#d3_select), css selector

> A selection is an array of elements pulled from the current document. D3 uses CSS3 to select elements. For example, you can select by tag ("div"), class (".awesome"), unique identifier ("#foo"), attribute ("[color=red]"), or containment ("parent child"). Selectors can also be intersected (".this.that" for logical AND) or unioned (".this, .that" for logical OR). If your browser doesn't support selectors natively, you can include Sizzle before D3 for backwards-compatibility.

## json构造的顺序


## join key not work

	jobsSelection = d3.select("#jobs > .btn-group")
			.selectAll(".btn")
			.data(jobs, function(d){return selectedRace + d.jobName});

这样就可以了: 为什么?

	jobsSelection = d3.select("#jobs > .btn-group")
			.selectAll(".btn")
			.data(jobs, function(d){return d.race + d.jobName;});


## render a table with d3