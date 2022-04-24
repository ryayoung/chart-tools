# `superheat()`
### A "super" correlation heatmap you can't find elsewhere

Traditional correlation heatmaps generated from Seaborn or Plotly are good at using color to distinguish positive from negative correlations. However, they _aren't_ very good at drawing your eyes towards the _strongest_ correlations. Especially with large datasets containing many variables, the chart gets cluttered with weak correlations that you don't care about.

Instead, with dynamically sized cells, the chart is far easier to read. Your eyes are instantly drawn to the most significant correlations.

<img width="1027" alt="Screen Shot 2022-04-24 at 1 16 21 AM" src="https://user-images.githubusercontent.com/90723578/164964749-ee0cfb9e-1774-49c9-830c-eeaf41848dc4.png">

Unfortunately, this chart is impossible to build with the "heatmap" or equivalent function provided in most popular graphing libraries, so instead, we have to build a scatterplot that looks and works like a heatmap. This is extremely awkward to do, and requires more code than anyone would normally want to write in their typical visualization workflow.
















This function is based on Drazen Zaric's "Better Heatmaps" in [this](https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec) article, and his [heatmaps](https://pypi.org/project/heatmapz/) package.
