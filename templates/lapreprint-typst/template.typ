#import "lapreprint.typ": *
#show: template.with(
  title: "[-doc.title-]",
[# if parts.abstract or parts.summary #]
  abstract: (
[# if parts.abstract #]
    (
      title: "Abstract",
      content: [
[-parts.abstract-]
      ]
    ),
[# endif #]
[# if parts.summary #]
    (
      title: "Plain Language Summary",
      content: [
[-parts.summary-]
      ]
    ),
[# endif #]
  ),
[# endif #]
[# if doc.subtitle #]
  subtitle: "[-doc.subtitle-]",
[# endif #]
[# if doc.short_title #]
  short-title: "[-doc.short_title-]",
[# endif #]
[# if options.short_citation #]
  short-citation: "[-options.short_citation-]",
[# endif #]
[# if options.heading_numbering #]
  heading-numbering: "[-options.heading_numbering-]",
[# endif #]
[# if options.theme #]
  theme: [-options.theme-],
[# endif #]
[# if doc.open_access !== undefined #]
  open-access: [-doc.open_access-],
[# endif #]
[# if doc.doi #]
  doi: "[-doc.doi-]",
[# endif #]
[# if doc.date #]
  date: datetime(
    year: [-doc.date.year-],
    month: [-doc.date.month-],
    day: [-doc.date.day-],
  ),
[# endif #]
[# if doc.keywords #]
  keywords: (
    [#- for keyword in doc.keywords -#]"[-keyword-]",[#- endfor -#]
  ),
[# endif #]
[# if doc.bibtex #]
  bibliography-file: "[-doc.bibtex-]",
[# endif #]
  authors: (
[# for author in doc.authors #]
    (
      name: "[-author.name-]",
[# if author.orcid #]
      orcid: "[-author.orcid-]",
[# endif #]
[# if author.affiliations #]
      affiliations: "[#- for aff in author.affiliations -#][-aff.index-][#- if not loop.last -#],[#- endif -#][#- endfor -#]",
[# endif #]
    ),
[# endfor #]
  ),
  affiliations: (
[# for aff in doc.affiliations #]
    (
      id: "[-aff.index-]",
      name: "[-aff.name-]",
    ),
[# endfor #]
  ),
[# if doc.venue.title #]
  venue: "[-doc.venue.title-]",
[# endif #]
[# if options.logo #]
  logo: "[-options.logo-]",
[# endif #]
[# if options.kind #]
  kind: "[-options.kind-]",
[# endif #]
  margin: (
[# if parts.acknowledgements #]
    (
      title: "Acknowledgements",
      content: [
[-parts.acknowledgements-]
      ],
    ),
[# endif #]
[# if parts.availability #]
    (
      title: "Data Availability",
      content: [
[-parts.availability-]
      ],
    ),
[# endif #]
  ),
)

[-IMPORTS-]

// Three-line (booktabs-style) table rendering.
// MyST emits tables as `tablex(...)` from @preview/tablex and spreads
// `..tableStyle` into the call. We override that empty default here so
// tablex draws no grid lines of its own, then wrap only the table body
// (not the whole figure, so the caption stays outside) in a block that
// draws the thick top and bottom rules.
#let tableStyle = (
  auto-hlines: true,
  auto-vlines: false,
  stroke: none,
  inset: (x: 8pt, y: 6pt),
  map-hlines: h => {
    if h.y == 1 {
      (..h, stroke: 0.5pt + black)
    } else {
      (..h, stroke: none)
    }
  },
)

#show figure.where(kind: "table"): it => [
  #block(
    stroke: (top: 1pt + black, bottom: 1pt + black),
    inset: (top: 4pt, bottom: 4pt),
    breakable: false,
    it.body,
  )
  #it.caption
]

[-CONTENT-]
