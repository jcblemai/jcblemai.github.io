---
title: "Use a seaborn color palette for plotly figures"
date: "2022-06-02T17:28:26"
lastmod: "2025-07-21T10:01:39"
draft: false
slug: "use-a-seaborn-color-palette-for-plotly-figures"
wordpress_id: 121
wordpress_type: "post"
wordpress_status: "publish"
wordpress_title: "Use a seaborn color palette for plotly figures"
wordpress_url: "https://josephlemaitre.com/2022/06/use-a-seaborn-color-palette-for-plotly-figures/"
author: "josephlemaitre"
categories: ["atomic"]
tags: ["python-fu"]
layout: "post"
permalink: "/2022/06/use-a-seaborn-color-palette-for-plotly-figures/"
published: true
render_with_liquid: false
---

If you choose carefully a seaborn color palette, such as:

    palette = sns.color_palette("Spectral", n_colors=n_clusters)

and you want to use it in a plotly figure, it's not as straightforward as it should. You need first to scale it and convert it first:

    palette_for_plotly = [f"rgb({c[0]*256}, {c[1]*256}, {c[2]*256})" for c in palette]

So you can have consistent colours scheme across all of your figures ✨

    fig = ff.create_choropleth(
        fips=labels.fips, values=labels.label,
        show_state_data=True,
        show_hover=True, centroid_marker={'opacity': 0},
        asp=2.9, title='County cluster',
        legend_title='cluster',
        colorscale=palette_for_plotly,
    )
