---
title: Article Title
subtitle: Subtitle of the article
short_title: Article
authors:
  - name: Author Name
    affiliations:
      - Affiliation
    email: author@example.com
abstract: |
  A one-paragraph abstract summarizing the article. Replace this placeholder with
  a concise description of the problem, approach, and key findings.
keywords:
  - keyword one
  - keyword two
exports:
  - format: pdf
    template: lapreprint-typst
    output: article.pdf
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

[**Download PDF**](article.pdf)

# Introduction

Welcome to this article. This section introduces the topic and explains who
the article is for and how it is organized.

## Who This Article Is For

This article is for anyone interested in the topic.

## How to Read This Article

Each section builds on the previous one. Start from the beginning and work
through to the end.

# Getting Started

This section introduces the fundamental concepts.

## Overview

Provide an overview of the topic here.

## Key Concepts

Explain the key concepts that readers need to understand.

```{code-cell} ipython3
print("Hello, World!")
```

## Key Tools

The table below shows an overview of the key tools used in this article.

```{list-table} Overview of key tools
:header-rows: 1
:name: tab-tools

* - Tool
  - Description
  - Version
* - Python
  - Programming language
  - 3.12
* - NumPy
  - Numerical computing library
  - 1.26
* - Matplotlib
  - Plotting and visualization
  - 3.8
* - MyST
  - Markdown authoring framework
  - 1.8
```

# Installation

This section covers how to set up your environment.

## Prerequisites

List the prerequisites here.

## Installation Steps

```bash
pip install numpy matplotlib
```

## Verifying the Installation

```{code-cell} ipython3
import sys
print(f"Python version: {sys.version}")
```

# Example

This section walks through a complete example.

## Setting Up

Describe the setup steps here.

## Sample Figure

{numref}`fig-sample` shows a sample bar chart generated with Matplotlib.

```{figure} images/sample_figure.png
:name: fig-sample
:alt: A sample bar chart

A sample bar chart showing values for five categories.
```

## Running the Example

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("sin(x)")
ax.set_title("A Simple Plot")
plt.show()
```

# Summary

This article demonstrated the basic workflow. Replace this section with your
own conclusions and next steps.

## Acknowledgements

Thank you to everyone who contributed to this article.
