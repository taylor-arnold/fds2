# Building the Practice Notebooks

Working notes for drafting `notebookNN.qmd` files for DSST389 (Advanced Data
Science). Each notebook is a set of in-class practice questions **with the
answers filled in**; the empty `.ipynb` versions students get are generated
from these later. Ask for "notebook37" and this file should be enough to
produce a draft in the right shape.

This is the nb389 counterpart to `nb289/NOTEBOOKS.md`. The two courses share a
book, a `data/` directory, and a house style, so most of the process below is
copied from there on purpose. Where nb389 differs — a course schedule that
starts numbering at 31, chapters that lean on one or two heavyweight corpora
instead of twenty independent tables, an API chapter with no dataset to pick
at all — the differences are called out explicitly rather than left implicit.
When in doubt about house style (chain formatting, how to phrase a written
question, how to verify a plot), look at how nb289 did it; the notebooks
already drafted there are the best reference available, now that `nb_old` is
gone.

## 1. Find the scope

Each notebook covers one class meeting, and each class meeting covers a
specific *range of sections* of one chapter. The mapping lives in the course
schedule at `/Users/admin/gh/courses/dsst389-f26/index.html`. Unlike nb289,
the notebook numbers do not restart at 1: DSST389 picks up where DSST289's
notebook numbering left off, so the first notebook of the semester is
`notebook30.qmd` (a Polars + plotnine review, already written) and the
chapter-based notebooks run 31 through 48.

There is no notebook44. The week it would occupy (2026-10-26 to 2026-10-28)
is Exam II followed by Project Workshop I, and neither has a notebook in the
schedule — the same kind of gap as nb289's missing notebook16.

| Notebook | Sections | Chapter file |
|---|---|---|
| 30 (already written) | review, no book sections | — |
| 31 | 11.1–11.5 | `11_spatial_data.qmd` |
| 32 | 11.6–11.8 | `11_spatial_data.qmd` |
| 33 | 11.9–11.10 | `11_spatial_data.qmd` |
| 34 | 11.11–11.15 | `11_spatial_data.qmd` |
| 35 | 12.1–12.9 | `12_apis.qmd` |
| 36 | 12.10–12.17 | `12_apis.qmd` |
| 37 | 13.1–13.6 | `13_temporal_data.qmd` |
| 38 | 13.7–13.12 | `13_temporal_data.qmd` |
| 39 | 14.1–14.4 | `14_text_annotations.qmd` |
| 40 | 14.5–14.10 | `14_text_annotations.qmd` |
| 41 | 15.1–15.3 | `15_text_vectors.qmd` |
| 42 | 15.4–15.5 | `15_text_vectors.qmd` |
| 43 | 15.6–15.7 | `15_text_vectors.qmd` |
| 45 | 16.1–16.5 | `16_network_data.qmd` |
| 46 | 16.6–16.10 | `16_network_data.qmd` |
| 47 | 17.1–17.6 | `17_image_data.qmd` |
| 48 | 17.7–17.9 | `17_image_data.qmd` |

To count the sections, count the `##` headings in the chapter file and skip
the ones inside a `::: {.callout-note}` block, which are not numbered, and
skip the final `## References {-}` / `## Summary` framing headings the same
way nb289 does. The Setup block is section X.1, so the Introduction is X.2
and the first real material is X.3. Two things worth knowing before you plan
a notebook:

- **Chapter 11 gets four notebooks, not one or two.** Spatial data is a big
  chapter (fifteen sections) and the course spends four class meetings on it.
  That is a real change from nb289, where at most two notebooks ever shared a
  chapter. See the dataset section below for what that does to dataset
  choice.
- **Callout asides sit exactly where nb289 warned they would.** `11_spatial_data.qmd`
  has "Why projections matter" folded into a callout between CRS (11.4) and
  Interactive Visualization (11.5), and "Other geometry types" folded in
  between Spatial Polygons (11.6) and Polygon Metrics (11.7). Both are easy to
  miscount if you go by `##` headings alone. `13_temporal_data.qmd` has two
  more ("Extracting date components", "Weekday and month names"), and
  `14_text_annotations.qmd` has one ("Installing the language model").
  `12_apis.qmd` has one near the end ("Versioning in the Action API"), after
  Reproducible Snapshots and before Conclusions — easy to miss because by
  then the chapter feels like it is winding down.

**Read the chapter sections before writing anything.** The section range is a
hard boundary in both directions, same as nb289. A notebook may use anything
from earlier chapters (1–10 included — these students took DSST289) freely,
but it must not reach for a method the students have not seen yet in *this*
book's order.

### Tool ledger

Cleared out, ready to fill in as notebooks are drafted. Notebook30 is a
review of material students already have from DSST289 and introduces nothing
new, so the ledger starts at notebook31. Add a row every time you draft a
notebook, the same way nb289 did: new material is the point of a notebook,
but a question that quietly requires something from three weeks ago is how
that something stops being a lookup and starts being a fact the student
knows. Chapters 1–10's tools (from nb289) are all fair game without a row
here — this ledger only needs to track what DSST389 itself introduces.

| Notebook | Sections | Tools and ideas introduced |
|---|---|---|
| 31 | 11.1–11.5 | the `geo` namespace registered by `import funs`, reachable as `.geo.<method>` on any Polars DataFrame; the `geometry` column as WKT text and the `_crs` helper column; building WKT by hand with `pl.format("POINT ({} {})", c.lon, c.lat)`, and that `POINT` is written longitude first, so swapping the order builds a valid but wrong geometry with no error; `.geo.points_from_xy(x, y)` as the safe way to build points and record a CRS (default EPSG:4326); coordinate reference systems and EPSG codes; `.geo.to_crs()` to reproject; `geom_map()` with `coord_fixed()` for a to-scale static map, against a plain `geom_point()` scatter, which has no CRS and no scale; `.geo.explore()` for an interactive Folium map, with `tooltip=` taking plain column name strings rather than `c.` expressions; chaining `.filter()` straight into `.geo.explore()` |

## 2. Pick the dataset

`dataset_description.qmd` is the catalogue: it describes every table in
`data/` and what its columns mean. It is the same file both courses read from
— nb389 does not get its own private data directory.

The three rules from nb289 still apply:

1. **Avoid the dataset the chapter itself uses.** Open the chapter's Setup
   block and pick something else.
2. **Let the topic pick the dataset, not the other way around.** A spatial
   chapter wants real polygons that actually touch and overlap; a network
   chapter wants an edge list with real hubs and real isolates; a chapter on
   an NLP pipeline wants raw, unannotated text, not a table someone already
   ran spaCy over.
3. **Prefer subjects students can reason about**, so they can tell a wrong
   answer from a right one without checking the back of the book.

A fourth rule is new to nb389 and is the reason this document exists in a
different shape than nb289's:

4. **A whole chapter may share one dataset if the chapter has more than two
   notebooks, or if the topic genuinely needs a dataset richer than the
   catalogue offers twice over.** nb289 could insist on a fresh table every
   notebook and a shared table only across a same-chapter pair, because
   chapters 1–10 are well served by twenty-odd unrelated CSVs. Chapters
   11–17 are not built that way. The book itself commits to one Wikipedia
   author corpus across five straight chapters (12 through 16), which is a
   sign that rich, chapter-appropriate alternatives are genuinely scarce for
   spatial, network, and cross-lingual text work — not a sign that the rule
   should be ignored. Chapter 11 alone has four notebooks; forcing four
   distinct spatial datasets on it would mean reaching for thin ones just to
   avoid repetition, which is worse than one rich family carried across all
   four. Reuse the way notebook14/15/17/18/19 already do in nb289 (a whole
   corpus, several tables, used for everything the chapter needs) rather than
   the way notebook10/11 do (one flat table). Still avoid reusing a dataset
   *nb289 already spent* on unrelated material if a comparably good
   unused option exists — but do not manufacture variety the catalogue does
   not support.

### What each chapter's own Setup block already uses

Checked directly against the Setup cells, since this is the thing to avoid
and it is easy to guess wrong:

| Chapter | Its own dataset |
|---|---|
| 11 Spatial Data | `data/acs_cbsa.csv` (US metro regions, ACS) |
| 12 APIs | none — it builds a corpus live over the network |
| 13 Temporal Data | `data/wiki/uk/*.parquet` — pageviews and revisions for the 376-page "Victorian and Irish novelists" corpus built in chapter 12 |
| 14 Text Annotations | `data/wiki_uk_meta.csv.gz` + `data/wiki_uk_authors_text.csv` — a *different*, smaller, pre-built corpus of 75 British authors (Chaucer to modern) |
| 15 Text Vectors | the same 75-author corpus as chapter 14, plus `data/wiki_uk_authors_text_fr.csv` for the cross-language section |
| 16 Network Data | `data/wiki_uk_citations.csv` + `data/wiki_uk_cocitations.csv` — again the 75-author corpus |
| 17 Image Data | `data/birds10.parquet` (Caltech-UCSD Birds) |

Two things worth flagging before you draft anything in this range:

- **Chapters 12 and 13 are not the same corpus as 14, 15, and 16**, even
  though all five are "Wikipedia authors" in spirit. 12/13 use the
  376-page corpus students watch get built live from two category tags;
  14/15/16 use a separate, pre-existing 75-author corpus. Avoiding "the
  chapter's dataset" for notebook37/38 (chapter 13) means avoiding
  `data/wiki/*`; avoiding it for notebook39/40/41/42/43/45/46 means avoiding
  `data/wiki_uk_*`. They are easy to conflate and worth double-checking
  against the table above rather than from memory.
- **Chapter 15's cross-language section (15.6–15.7, notebook43) is a real
  constraint, not a preference.** `wiki_uk_authors_text_fr.csv` is the
  *only* French-paired text in the whole catalogue, and it is a translation
  of the same 75-author corpus the chapter itself uses. There is no second
  bilingual pair to swap in. When you draft notebook43, either accept a
  narrower slice of the same corpus than the chapter uses (different authors,
  a different question) and say so plainly, or treat the constraint itself as
  worth a written question ("why is finding a second parallel corpus harder
  than finding a second English one?"). Don't paper over it by pretending an
  alternative exists.
- **Chapter 12 has no dataset to avoid, because avoiding the book's dataset
  *is* the exercise.** Notebook35/36 should define and collect a small,
  different Wikipedia population live over the API — a different category
  (or two) than `Category:Victorian novelists` / `Category:19th-century Irish
  novelists`, small enough to collect politely in one sitting. Notebook35
  (12.1–12.9: population definition through article text) and notebook36
  (12.10–12.17: links through conclusions) should share the one population
  they collect, the same way nb289's chapter-pair notebooks share a table —
  collecting a second population for notebook36 would just mean re-running
  the whole pipeline for no pedagogical reason. This is also a dry run for
  the final project, which asks students to do the same thing at a larger
  scale (75–250 pages) a few weeks later, so a population that is genuinely
  theirs to explore, rather than a copy of the book's, is worth the extra
  thought.

### Candidate pools by topic

Pulled from the `<img>` tags in `dataset_description.qmd`, which mark
datasets the catalogue itself considers spatial, temporal, text, network, or
vision. Cross-reference against the "already spent" list in nb289's own
ledger (Wikipedia authors, English Wikipedia, and SCOTUS were flagged there
as **unused** by any DSST289 notebook) — those three are free for nb389 to
claim.

- **Spatial** (chapter 11, four notebooks): `countries.csv` + `countries_polygons.geojson`
  + `countries_cities.csv` (points, polygons, and a joinable cities table all
  at once); the France family (`france_departement_*`, `france_cities.csv`,
  `france_departement_sml.geojson`); the Italy family
  (`it_province_covid.csv`, `it_cities.csv`, `it_province.geojson`); Paris
  Métro stops; US city population; storms; RVA flights. The France and Italy
  families are the strongest single-corpus candidates for carrying all four
  notebooks, since each pairs points, real polygons, and a population table
  in one place — exactly what buffers, dissolving, exploding, and simplifying
  need in notebook34.
- **Temporal** (chapter 13, two notebooks): storms (six-hour cadence over 70
  years); RVA flights + weather (hourly, one year); the France/Italy COVID
  series (daily); US city population (a panel, but only 23 time points —
  thin for rolling-window work); the keylog data (millisecond-resolution
  keystrokes, 1.1M rows, real durations and real pauses to compute). Keylog
  is the one dataset in the whole catalogue built for exactly this kind of
  question and is otherwise unused.
- **Text** (chapters 14–15, five notebooks total): Shakespeare's raw lines
  (unannotated — a genuine NLP-pipeline target, unlike `shakespeare_words.csv`
  which is pre-tagged); the classification corpora (IMDb, AG News, Amazon,
  BBC, SST, GoEmotions) all carry a raw `text` column under the trimmed
  preview in the catalogue; SCOTUS case text. Remember the cross-language
  constraint above before committing chapter 15's dataset.
- **Network** (chapter 16, two notebooks): English Wikipedia (`enwiki_articles`,
  `enwiki_links_p1/p2`, `enwiki_distance` — 10 million edges, real hubs) and
  SCOTUS (`scotus_citation.csv`, 230,000 edges of legal precedent). Both are
  flagged unused in nb289's ledger and both are exactly what a citation
  network chapter wants; picking between them is a question of scale
  (SCOTUS is small enough to look at directly, enwiki is not) rather than of
  fit.
- **Vision** (chapter 17, two notebooks): FSA-OWI color photographs (already
  used once in nb289's notebook17, but for a completely different lesson —
  reading imperfect files, not embeddings — so reuse here is not repetition);
  MNIST/EMNIST/Fashion-MNIST; Imagenette/Imagewoof (both ship pre-computed
  `vit` and `siglip` embeddings, which is exactly what notebook48's transfer-learning
  and zero-shot sections need without asking students to run a model
  themselves); Oxford Flowers. Imagenette or Imagewoof are the strongest fit
  for notebook48 specifically, since the embeddings are already sitting in
  the table.

### Dataset ledger

Cleared out. Fill in as each notebook is drafted, the way nb289 did — and
once a row is added, write a paragraph below the table (nb289-style) about
*why* that dataset earned the notebook, not just what it is. That paragraph
is what keeps the next person from re-picking a dataset that already failed
for a documented reason.

| Notebook | Dataset | File |
|---|---|---|
| 31 | Italian cities | `data/it_cities.csv` |

Notebook31 takes the Italy family's point table, `it_cities.csv`: 388 cities
and towns, each with a name, longitude, latitude, and population. It was
picked over the France family mainly because it is cleanly unused; nb289's
notebook05 already spent `france_departement_covid.csv`, a different table
from the same family, on unrelated material, and Italy carries no such claim
anywhere in either course. That made it the safer anchor for all four
chapter-11 notebooks. The table itself earns the
points-only sections specifically: no missing values, a population column
with a real (and checkable) top six, and a latitude range wide enough
(37°N to 47°N) to make the CRS discussion concrete without needing the
polygons that only show up starting in notebook32. It also has a genuine
seam worth teaching around: the data stops at a 20,000-population floor
instead of covering all ~7,900 Italian comuni, which notebook31's closing
question uses directly.

## 3. Write the file

Filename `notebookNN.qmd` at the repo root, next to `notebook30.qmd`, which
is the canonical format for this course (nb289's `notebook_example_format.qmd`
no longer exists — `nb_old` was removed — so notebook30 is the reference
now). Header is YAML frontmatter, not a `##` heading:

```
---
title: "NotebookNN"
solutions-release-date: "YYYY-MM-DD"
---
```

Set `solutions-release-date` to the class date for that notebook from the
course schedule (e.g. notebook37 is 2026-09-23). Then `### Setup`, then
`### Questions` — three `#`s, matching notebook30.qmd exactly, not the two
`#`s nb289's own instructions describe (that instruction was already out of
sync with nb289's actual files; don't propagate the mismatch here).

The setup blocks are fixed boilerplate — copy them from `notebook30.qmd` and
change only the data-loading cell:

````
```{python}
#| tags: [noclear]
#| eval: false
! wget -q -nc https://raw.githubusercontent.com/taylor-arnold/fds2/refs/heads/main/funs.py
```

```{python}
#| tags: [noclear]
import polars as pl
from plotnine import ggplot, aes
from polars import col as c

import funs

ub = "https://raw.githubusercontent.com/taylor-arnold/fds2/refs/heads/main/"
```

```{python}
#| tags: [remove]
#| include: false
ub = ""
```

```{python}
#| tags: [noclear]
<name> = pl.read_csv(ub + "data/<file>.csv")
```
````

Chapters 11 and 17 will need extra imports in this cell (`funs`' `geo`
namespace registration for spatial work, `DSImage`/`cv2`/`PIL` for image
work) — copy those from the relevant chapter's own Setup block, not from
notebook30. Chapter 12's setup cell looks different again: instead of loading
a table, it sets up `requests` + `requests_cache` the way `12_apis.qmd`
does, since there is nothing to `pl.read_csv()` yet.

The load cell may quietly clean the data with methods the students have not
met yet, same as nb289. Leave in the mess the chapter is *about*.

Open `### Questions` with a short paragraph introducing the dataset: what a
row is, what the columns mean, any unit that is not obvious. For chapter 12,
this paragraph instead introduces the population being collected and why it
was chosen. Then say results should be printed, not saved, unless a question
says otherwise.

## 4. Shape the questions

Ten to twelve numbered questions, same target as nb289. The arc runs from a
one-method question to a short pipeline, following the chapter's own order of
presentation.

Write each answer as a chain in the book's house style: parentheses on their
own lines, one method per line, four-space indent, `c.` column references.

Carried over from nb289, still true here:

- **A written question or two.** Make students look at the data or the
  network or the map, not just run code against it.
- **A deliberate failure.** Showing the trap beats warning about it.
- **Old tools inside new questions.** A `.filter()` from chapter 5, a `.join()`
  from chapter 8 — DSST389 students have the whole first book behind them,
  so the pool to draw "old tools" from is larger here than it ever was in
  nb289, not smaller.
- **A remark about the data itself**, where the data earns it.

Three notes specific to this course's chapters:

- **Chapter 12's live calls need to be polite by construction, not by
  reminder.** Cache every request (`requests_cache`, as the chapter itself
  does) before writing a single question, and size the population small
  enough that a full re-run of notebook35 and notebook36 back-to-back is
  fast and does not hammer the API. A question that tells a student to loop
  over hundreds of pages without a cache in front of it is a question that
  will get someone's IP rate-limited during a lab.
- **A rendered map is not a verified map.** Same lesson nb289 learned the
  hard way with plots in general (section 5 there), but spatial work adds a
  failure mode plots don't have: a CRS mismatch or an empty spatial join can
  produce a plot that renders without error and shows nothing where the data
  should be. Save and look at it.
- **Embeddings and NLP pipeline output are worth spot-checking against
  something you already know**, the same way nb289 checked Mesquite's own
  census rows before trusting a windowed growth rate. A nearest-neighbor
  query in embedding space, a KWIC line, or a named-entity list is only
  useful in a notebook if it is checked against text a reader can verify by
  eye, not just printed and trusted.

## 5. Verify before handing it over

Extract and execute every code block in order, same procedure as nb289:

```bash
uv run python - <<'EOF'
import re
src = open("notebookNN.qmd").read()
blocks = re.findall(r"```\{python\}\n(.*?)```", src, re.S)
g = {}
for i, b in enumerate(blocks):
    if "eval: false" in b:
        continue
    code = "\n".join(l for l in b.splitlines() if not l.startswith("#|")).strip()
    try:
        res = eval(code, g) if code.startswith("(") else exec(code, g)
        print(f"[{i}] OK", getattr(res, "shape", ""))
    except SyntaxError:
        exec(code, g); print(f"[{i}] OK")
    except Exception as e:
        print(f"[{i}] ERROR: {type(e).__name__}: {e}")
EOF
```

Then check every number that appears in the prose against the data, and
render every plot or map before describing it — nb289's whole section 5 on
this (numbers that rot, sorted results whose top row needs checking against
the raw rows behind it, prose written from plausibility rather than the
data, `.print(n)` eliding the row that matters) applies here without
modification, and is worth re-reading before drafting starts rather than
re-derived from scratch.

A few additions for chapters that don't exist in nb289's range:

- **Re-run chapter 12 notebooks from a cold cache before handing them over.**
  A live API call that succeeded once while drafting can 404, redirect
  differently, or get rate-limited on a second run. If the notebook depends
  on the exact shape of a live response, that dependency needs to survive a
  re-run days later, not just the one that produced the numbers in the prose.
- **A spatial join or a `.geo` method that returns an empty result does not
  raise an error.** Check row counts before and after, the same
  `.n_unique() == len()`-style discipline nb289 used for join keys, applied
  to geometries instead.
- **Image cells need to be looked at, not just executed.** A `PIL.Image` or
  `cv2` array that decodes without error can still be the wrong crop, the
  wrong channel order, or a broken filepath rendering as a blank tile.
- **spaCy's model needs to actually be loaded** (`en_core_web_sm`, per the
  chapter's own Setup) before any pipeline question is verified — a pipeline
  running against unloaded or mismatched model output will produce POS tags
  and dependency parses that execute cleanly and mean nothing.

Log new lessons here as they come up while drafting, the same way nb289 grew
its own section 5 over twenty notebooks. This document is expected to keep
changing as notebook31 through notebook48 actually get written.
