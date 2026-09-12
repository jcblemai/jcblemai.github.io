---
title: "Zsh and bash pitfalls"
date: "2023-05-05T18:24:55"
lastmod: "2025-07-21T10:01:39"
draft: false
slug: "zsh-and-bash-pitfalls"
wordpress_id: 176
wordpress_type: "post"
wordpress_status: "publish"
wordpress_title: "Zsh and bash pitfalls"
wordpress_url: "https://josephlemaitre.com/2023/05/zsh-and-bash-pitfalls/"
author: "josephlemaitre"
categories: ["Non classé"]
tags: []
layout: "post"
permalink: "/2023/05/zsh-and-bash-pitfalls/"
published: true
render_with_liquid: false
---

zsh is sometime touted as a drop-in replacement for bash. But it is not. When running our same scenario pipeline code on our cluster and on my macbook, I painfully discovered that

while this work on bash, it will return an error "= not found" on zsh

if \[ $RESUME\_DISCARD\_SEEDING == "true" \]; then

and should be corrected to

if \[\[ $RESUME\_DISCARD\_SEEDING == "true" \]\]; then

mind the whitespace

<img src="/wp-content/uploads/2023/05/Screenshot-2023-05-05-at-17.04.53-1024x221.png" class="wp-image-178" />

Moreover, while

for filetype in "seed spar snpi hpar hnpi"

iterates through all "space separted filetypes (seir, snpi), it does so in zsh only the option you run

setopt shwordsplit

before, which is usually not done in zshrc

so yeah... one more reason to hate computers.
