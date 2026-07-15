# Building the Practice Notebooks

Working notes for drafting `notebookNN.qmd` files. Each notebook is a set of
in-class practice questions **with the answers filled in**; the empty `.ipynb`
versions students get are generated from these later. Ask for "notebook09" and
this file should be enough to produce a draft in the right shape.

## 1. Find the scope

Each notebook covers one class meeting, and each class meeting covers a specific
*range of sections* of one chapter. The mapping lives in the course schedule at
`/Users/admin/gh/courses/dsst289-f26/index.html`. Note that the class order is
not the book order (chapter 9 is split around chapters 10 and 8):

| Notebook | Sections | Chapter file |
|---|---|---|
| 01 | 1.1–1.7 | `01_intro.qmd` |
| 02 | 1.8–1.10 | `01_intro.qmd` |
| 03 | 2.1–2.6 | `02_organize.qmd` |
| 04 | 2.7–2.11 | `02_organize.qmd` |
| 05 | 3.1–3.9 | `03_types.qmd` |
| 06 | 4.1–4.3 | `04_graphics.qmd` |
| 07 | 4.4–4.8 | `04_graphics.qmd` |
| 08 | 5.1–5.5 | `05_group.qmd` |
| 09 | 5.6–5.9 | `05_group.qmd` |
| 10 | 6.1–6.5 | `06_window.qmd` |
| 11 | 6.6–6.9 | `06_window.qmd` |
| 12 | 7.1–7.6 | `07_graphics_ii.qmd` |
| 13 | 7.7–7.10 | `07_graphics_ii.qmd` |
| 14 | 9.1–9.4 | `09_restructure.qmd` |
| 15 | 10.1–10.5 | `10_collect.qmd` |
| 17 | 10.6–10.10 | `10_collect.qmd` |
| 18 | 8.1–8.6 | `08_combine.qmd` |
| 19 | 8.7–8.9 | `08_combine.qmd` |
| 20 | 9.5–9.8 | `09_restructure.qmd` |

(There is no notebook16; that class is a project workshop.)

To count the sections, count the `##` headings in the chapter file and skip the
ones inside a `::: {.callout-note}` block, which are not numbered. The Setup
block is section X.1, so the Introduction is X.2 and the first real material is
X.3. This is worth getting right before you plan any questions: it is the
difference between notebook06 covering the whole of the point geometry (which it
does) and covering optional aesthetics as well (which belong to notebook07).

**Read the chapter sections before writing anything.** The section range is a
hard boundary in both directions. A notebook may use anything from earlier
chapters freely, but it must not reach for a method the students have not seen
yet, even when that method would be the natural way to answer a question. When
notebook03 needed "one film per country" it had to sort and take heads, because
`.unique()` belongs to 2.7 and lands in notebook04. Check the *next* notebook's
range to see what you are saving for it.

### Tool ledger

What each notebook's reading introduced. Add a row whenever you draft one, so
that later notebooks know what students already have in hand and can keep asking
them to use it. New material is the point of a notebook, but a question that
quietly requires a `.filter()` from three weeks ago is how that filter stops
being something they look up and starts being something they know.

| Notebook | Sections | Tools and ideas introduced |
|---|---|---|
| 03 | 2.1–2.6 | `c.` column references; method chains in the house style; `.sort()` (multi-column, `descending=`); `.select()`, `.drop()`; `.head()`, `.tail()`, `.sample()`; `.drop_nulls()`, `.drop_nans()`; `.filter()` with `==`, `!=`, `>=`, `&`, `|`, and `.is_in()` |
| 04 | 2.7–2.11 | `.rename()`; `.unique()` with `subset=` and `keep=`; `.with_columns()` (several at once, overwriting a column); column math and methods such as `.sqrt()`, `.abs()`, `//`; `.pipe()`; the `.print(n)` helper from `funs.py`; `pl.when().then().otherwise()`, chained, with `pl.lit()` for text labels |
| 05 | 3.1–3.9 | `.schema` and the four core types (`str`, `i64`, `f64`, `bool`); why a stray `"NA"` turns a numeric column into text; `.cast()` with `strict=False`; `null` versus `NaN`; `.is_null()`, `.is_nan()`, `.fill_null()`, `.fill_nan()`; expressions as objects that can be named and reused across contexts; `.str` methods, notably `.str.to_date()` and `.str.to_uppercase()` |
| 06 | 4.1–4.3 | the grammar of graphics: a plot is a dataset, a set of aesthetic mappings, and a geometry; `.pipe(ggplot, aes(x, y))` followed by `.geom_point()`; mapping a column to the x and y aesthetic; putting `.filter()`, `.sort()`, and `.with_columns()` *before* the `.pipe()` so that manipulation and plotting are one chain |
| 07 | 4.4–4.8 | optional aesthetics mapped inside a second `aes()` within the geometry (`color=`), versus fixed values set outside it (`alpha=`, `color="#F5276C"`, `size=`, `nudge_y=`); why an `i64` column gets a continuous color bar and a `str` column gets discrete swatches; `.geom_text()` with the `label=` aesthetic; `.geom_line()`, which connects rows in x-order rather than row order; `.geom_col()` with `.coord_flip()`, whose bars follow the row order of the data; the `data=` argument for giving one geometry its own table; `.labs()` |
| 08 | 5.1–5.5 | `.group_by()`, and the fact that it computes nothing: it returns a `GroupBy` promise that the next method has to consume, so there is no grouped table and nothing to ungroup; `.head(n=1)` on a group, and the sort-then-take-the-top-row-of-each-group move; `.agg()` with named results; `pl.len()`; `.mean()` and `.median()` inside `.agg()`; `maintain_order=True` and why group order is otherwise unstable; grouping on several columns at once; aggregating an *expression* rather than a column, e.g. `(c.rent_1br_median > 1200).sum()` to count trues in a boolean; aggregating and then plotting the small result |
| 09 | 5.6–5.9 | `.count()` (non-missing values) against `pl.len()` (rows), and reading a group mean next to its count; `.n_unique()` as the test of whether a column identifies a row; whole-frame summaries with aggregating expressions inside `.select()`, since `.agg()` exists only on a `GroupBy`; `.min()`, `.max()`, `.quantile()`, `.sum()`, `.first()`; `pl.corr()`; aggregation as row reduction, and the fact that `.max()` returns the number but loses the film; that `.max()` skips nulls while `.sort()` puts them first, so `.first()` after a descending sort can disagree with `.max()` in the same `.agg()` |
| 10 | 6.1–6.5 | `.over()` after an aggregation, inside `.with_columns()` (the group's answer written onto every row) and inside `.filter()` (computed, compared, discarded); the same expression in three contexts, `agg` versus `over`, and that only `over` keeps the rows a within-group comparison needs; `pl.len().over()` as a group size on every row; windowing on the group column versus on the time column (`.over(c.state)` against `.over(c.year)`); `.shift(1)` and why it must sit after a `.sort()` and be scoped with `.over()` or it walks across group boundaries; `NaN` and `inf` from dividing by zero, and that neither is a `null`, so `.drop_nulls()` does not catch them and `NaN` sorts to the top; that filtering *before* a window silently redefines "the row above", so the filter belongs after the shift; `.forward_fill()` and `.backward_fill()` with `.over()`, and a fill as a guess that brackets the truth |
| 11 | 6.6–6.9 | `.rank()`, which reads values and ignores row order, and defaults to rank 1 for the *smallest* value unless you pass `descending=True`; ranking within a group (`.over(c.state)`) versus within a time slice (`.over(c.year)`), and rank movement by shifting the rank column; ties averaged, so ranks come back as floats and a column of placeholder zeros gets ranked too; `.cum_sum()`, where the sort *is* the result, and a running total next to a fixed `.sum()` in the same expression; `.cum_sum().over()` to restart the accumulation per group; `.rolling_mean(window_size=)`, which needs both the sort and the `.over()`, and ruins `window_size - 1` rows per group when the `.over()` is missing; smoothing as the removal of information rather than the addition of any; `.geom_line()` on a windowed column, and windowing before filtering so the denominator stays the whole table |
| 12 | 7.1–7.6 | statistical geometries as a `group_by` and `agg` in disguise, drawing the result of a computation rather than one shape per row; `.geom_bar()`, which takes one categorical aesthetic and counts the rows itself, against `.geom_col()`, which takes an `x` and a `y` and draws the height you give it, so a mean can only be drawn by the second; `.coord_flip()`; that a categorical axis follows the order the values *first appear in the data*, with no ordering step inside the plot, so ordering a chart means sorting the table, either on an aggregated column or, when the number exists only inside the plot, on a window aggregate (`.sort(pl.len().over(c.meal_name))`, `.sort(c.kcal.median().over(c.meal_name))`); `.cast(pl.String)` to make an integer column categorical, and why the `.sort()` has to come before the cast; `.geom_histogram()` with `binwidth=` and `boundary=`; `.geom_density()` with `adjust=`; `.geom_boxplot()`; `.geom_smooth(method="lm", se=False)` |
| 13 | 7.7–7.10 | scales as the layer between a column and what you see; `.scale_color_cmap_d()` for a categorical color and `.scale_color_manual(values={...})` to set one color per category; that a color scale is a categorical axis, so a `.sort()` fixes the legend order; `.scale_x_log10()` for a skewed column, and that it *cannot draw a zero*, so it silently drops rows; `.scale_x_continuous()` / `.scale_y_continuous()` with `breaks=` and `limits=`, and that `limits=` is a filter rather than a zoom (it deletes rows outside the range and refits any stat on the survivors), against `.coord_cartesian(xlim=, ylim=)`, which crops; `.facet_wrap()` with `show_legend=False` on a redundant color; `.facet_grid()` on two variables, and the `scales=` argument that makes panels legible by making them incomparable; `.labs()` with `title=`, `subtitle=`, `caption=`; `.theme_tufte()` and themes as the non-data layer; the best-practice list of 7.10, met by breaking it |
| 14 | 9.1–9.4 | **no new methods.** The class is conceptual and everything in it is chapters 1–7 pointed at a new question. The *unit of observation* as the "who or what" a row stands for, and as a claim you can test rather than a label you assign; the primary key as that test, run with `.n_unique()` against `pl.len()` inside a `.select()`; compound keys, confirmed when `group_by(a, b).agg(n = pl.len()).filter(c.n > 1)` returns nothing; that a `group_by` on a non-key *pools* instead of failing, so a broken key hands back a plausible ranking rather than an error; the three tidy rules (one variable per column, one observation per row, one unit per table) and the fact that tidiness is relative to the unit you need; a variable packed into a cell (`"3.1.64"`) and what the packing costs, since a text sort puts 3.1.10 before 3.1.2; a cell holding a *set* of values rather than one; a column whose `n_unique()` is 1, which is not a variable at all and which no tidy rule can catch; aggregation as the only shape-change they already own, and as the one that runs downhill only |
| 15 | 10.1–10.5 | **no new methods**, and for the second class running. Everything is chapters 1–7 plus notebook14's key test, pointed at a schema instead of a question. The rule that only data describing the *whole* unit of observation belongs in a table, and the fact that it is a rule you run rather than a rule you eyeball: `group_by(g).agg(c.x.n_unique())` is the test, and a column that never varies within its group (`line_color`) is a fact about the group stored once per row, while a column that does vary (`lon`, `lat`) is a fact about the unit and belongs where it is; the second table as the place the invariant column goes, built with `.unique(subset=, keep=)`; a placeholder string (`"NA"`) in a numeric column as a storage decision that costs you the type, and `.cast(strict=False)` as the repair; a stored *derived* column, checked against `.shift(-1).over()` and found to be a copy of another row's data; row order as the carrier of a variable nobody wrote down, and therefore as something no `.sort()` will preserve and no column records; `.scale_color_manual()` fed from a palette dict built out of the split-out `lines` table; the column type as a decision about what can be recorded at all, since an `i64` line column cannot hold "3bis"; a synthetic key as what you need when the only identifier is a display name; denormalization as a *trade* (no joins needed, ever) rather than a mistake |
| 17 | 10.6–10.10 | `pl.read_csv()` as a short investigation rather than a function call: `separator=`, `skip_rows=`, `encoding=`, `null_values=`, and `schema_overrides=` as `null_values`' sibling (both prevent damage at read time instead of repairing it after, which is the distinction chapter 3 promised and deferred to here); reading a file's *raw lines* by handing `read_csv` a separator the file does not contain (`separator="\t"`, `has_header=False`, `quote_char=None`) so you can look before you guess; `encoding="utf8-lossy"` as the fix that removes the error and silently corrupts 98 captions, against `encoding="windows-1252"` as the fix that decodes them; that `encoding=` maps bytes to characters and therefore cannot touch an HTML escape like `&amp;`, which needs `.str.replace_all()`; `.str.contains()`, `.str.ends_with()`, `.str.replace_all()`; `.item(row, col)` to print a whole string past Polars' 30-character cell truncation; `pl.date(y, m, 1)` to make a plottable date out of a year and a month, and why that invented day is fine in a chart and a lie in a file; the data dictionary as the record of everything a file cannot say about itself |
| 18 | 8.1–8.6 | the primary/foreign key distinction as a fact about the *table* rather than about the column, tested with `.n_unique() == len()` before any join is written; `.join()` with `on=`, called as a method of the foreign-key (left) table; `left_on=`/`right_on=` when the key is named differently on each side (`dest` against `faa`); the default inner join as a silent row filter, and `how="left"` as the repair; `suffix=` to name a colliding column, on a `year` that means the year of the flight in one table and the year the aircraft was built in the other; a list passed to `on=` for a multi-column key; the filtering joins, `how="anti"` to hand back the rows that failed to match (so they can be grouped and explained) and `how="semi"` to ask which part of a lookup table is actually used; that a `null` key matches nothing, so the cancelled flights drop out of an inner join too |
| 19 | 8.7–8.9 | the fan-out: a right-hand key that repeats multiplies the left table, silently, and the row count is the only thing that says so, so the `.n_unique() == len()` check belongs *before* the join rather than after; that aggregating the right table until its key is unique is the repair, and that the grain you aggregate to is the grain you can join at; `.join_asof()` with `strategy="backward"`, which matches the most recent value rather than the equal one and therefore *cannot fail*, returning one row per left row however far away the match is; `coalesce=False` to keep the matched row's own key so the distance can be measured, and the rule that an asof join must always be followed by a look at that distance; that both tables must be sorted by the join key first; `pl.datetime(y, m, d, h, mi)` as `pl.date`'s sibling; `.join_where()` with several inequality expressions, the `_right` suffix for the other side, a table joined *to itself* to ask a question about pairs of rows, and `c.key < c.key_right` as the idiom that both stops a row pairing with itself and de-duplicates the symmetric pairs; `.over()` against agg-then-join as two routes to the same column, and the structural difference that decides between them, namely that `.over()` can only group rows already in the table, so a summary computed from *another* table has to be a join |
| 20 | 9.5–9.8 | `.pivot()` with `index=`, `on=`, `values=`, and the fact that the new column names appear in the order the values are *first seen*, so a `.sort()` has to come before the pivot (notebook12's categorical-axis rule, arriving on a column header); a pivot with holes in it, since a combination absent from the long table becomes a `null` cell, and `.fill_null(0)` as a claim about *why* it was absent rather than a formatting step; `.unpivot()` with `index=`, `variable_name=`, `value_name=`, and that the unpivoted variable comes back as a `str` because it was a column name; pivot and unpivot as a round trip that computes nothing, against aggregation, which runs downhill only; unpivoting *before* plotting, because a variable trapped in column names cannot be mapped to an aesthetic; `.str.split()` to make a list column and `.explode()` to give each element its own row; explode as the tool for a cell holding a **set** (three speakers) and the wrong tool for a cell holding a **record** (act, scene, line), which needs explode-*then*-pivot; `.cum_count()`, **introduced here**, as `.cum_sum()`'s row-counting sibling, used with `.over()` to number the exploded pieces so the pivot knows which column each one belongs in |

## 2. Pick the dataset

**One dataset per notebook, and a different one for each notebook.** Students
should get a new corner of the corpus each week rather than watching the same
table for a semester. `dataset_description.qmd` is the catalogue: it describes
every table in `data/` and what its columns mean.

Three rules for choosing:

1. **Avoid the dataset the chapter itself uses.** Open the chapter's Setup block
   and pick something else. The notebook is practice, not a re-run of the
   lecture, and a fresh table forces students to read column names rather than
   recall answers.
2. **Let the topic pick the dataset, not the other way around.** The dataset
   should make the chapter's ideas *visible*. Chapter 3 is about broken types, so
   notebook05 uses the French COVID data, where the counts really did arrive as
   strings full of `"NA"` and Corsica's département codes (`2A`, `2B`) really do
   break a cast to integer. A tidy table would have made that chapter feel like
   a formality. Grouping chapters want a table with a good categorical column;
   window chapters want a meaningful row order; joining chapters want a family of
   tables that actually link.
3. **Prefer subjects students can reason about** — films, food, countries,
   storms, cities — so they can tell a wrong answer from a right one without
   checking the back of the book.

Consecutive notebooks on the same chapter (03/04, 06/07, …) may reuse one dataset
across the pair, since the second class continues the first. That is what
notebooks 03 and 04 do with the Criterion films. Otherwise, move on.

### Dataset ledger

Keep this current so we do not repeat ourselves.

| Notebook | Dataset | File |
|---|---|---|
| 01 (example format) | food | `data/food.csv` |
| 03 | Criterion films | `data/criterion.csv` |
| 04 | Criterion films (continued) | `data/criterion.csv` |
| 05 | French département COVID | `data/france_departement_covid.csv` |
| 06 | U.S. storms | `data/storms.csv` |
| 07 | U.S. storms (continued) | `data/storms.csv` |
| 08 | US metro regions (ACS) | `data/acs_cbsa.csv` |
| 09 | Fifty Years of Movies | `data/movies_50_years.csv` |
| 10 | US city populations | `data/us_city_population.csv` |
| 11 | US city populations (continued) | `data/us_city_population.csv` |
| 12 | What We Eat in America | `data/wweia_food.csv` |
| 13 | What We Eat in America (continued) | `data/wweia_food.csv` |
| 14 | Shakespeare (all four tables) | `data/shakespeare_{plays,characters,lines,words}` |
| 15 | Paris Métro stops | `data/paris_metro_stops.csv` |
| 17 | FSA-OWI color photographs, as a legacy export | `data/fsac_export.csv` (built from `data/fsac.csv`) |
| 18 | RVA flights, all five tables | `data/flightsrva_{flights,airlines,airports,planes,weather}.csv.gz` |
| 19 | RVA flights (continued) | `data/flightsrva_{flights,airlines,airports,planes,weather}.csv.gz` |
| 20 | Shakespeare again, three of the four tables | `data/shakespeare_{plays,characters,lines}` |

Datasets the book leans on heavily and that are therefore lower priority for
notebooks: `countries.csv` (chapters 1–3), `food.csv`.

Strong unused candidates: Wikipedia authors, English Wikipedia, SCOTUS.

Ruled out: `majors.csv` looks promising in the catalogue and is not. It is a long
percentile table with three columns (major, percentile, earnings), so it has no
categorical column to group on and its "distribution" per major is a percentile
curve rather than a sample, which a boxplot would quietly misrepresent.

Notebooks 06 and 07 share the storms table, as the chapter pair allows. The two
companion tables, `storm_codes.csv` and `storm_gender.csv`, are still unused. They
were once penciled in for the joining chapter and are not the right call there:
notebook18 would have been the third notebook on the storms, and the joining chapter
wants tables whose keys can *fail*, which is what the flights corpus provides and a
pair of clean two-column lookups does not.

Notebook08 takes the ACS metro table. Chapter 11 also uses it, but no notebook
covers chapter 11, so nothing collides. It earned the grouping chapter on two
counts: `division` and `quad` give a nine-way and a five-way split of clean,
complete rows, and the file arrives sorted by population, which means a
`.group_by().head(n=1)` with no sort in front of it returns the largest metro in
each division and looks like a correct answer. That accident is the deliberate
failure notebook08 opens with.

Notebook09 could have stayed with the ACS table, as the chapter pair allows, and
did not, because that table has no missing values anywhere. Section 5.6 is built
on the difference between `pl.len()` and `.count()`, and with complete data the
two are the same number and the lesson is a definition rather than a finding. So
notebook09 takes Fifty Years of Movies, where Metacritic scores run from 73 of the
1970s films to 445 of the 2010s ones (the site launched in 2001), and the films
that did get a retroactive score are the memorable ones, which makes the decade
means quietly incomparable. **When a chapter is about missingness, choosing the
dataset means choosing the holes.** The same table has 495 films with no recorded
gross, which is what makes notebook09's closing trap work.

Notebook10 takes the US city populations, which is a panel: 289 cities by 23
censuses, one row each, so it has both of the things chapter 6 needs. The cities
give `.over(c.state)` something to group on and the censuses give `.shift()` a row
order that means something, and because the table is a rectangle you can window on
either axis, which is how notebook10 gets to ask for a city's share of its state
and then a city's share of its census year with the same expression. The mess worth
keeping is the zeros: a city that did not exist yet is recorded as `0`, not `null`,
and population is in thousands to one decimal, so a village of forty people is also
recorded as `0`. Dividing by that zero is what produces the `NaN` and `inf` that
`.drop_nulls()` cannot catch.

Notebook11 keeps the same table, as the chapter pair allows, and the zeros keep
earning their place: `.rank()` ranks the placeholders too, so the 73 cities recorded
as `0` in 1900 tie with each other and all take rank 253. The table also has a
century of American urban history in it that the students can check against what they
already know, which is what makes the results falsifiable: the rank movers from 1900
to 2010 are Sun Belt cities up and Massachusetts mill towns down, and Detroit goes
4th in 1920 to 18th in 2010. Worth knowing before you write about New York on this
table: the city annexed Brooklyn in 1898, Brooklyn is not a separate row, and so the
1.9 million people New York "adds" between 1890 and 1900 are mostly a boundary change
rather than growth. Notebook11 closes on that.

Notebook12 takes What We Eat in America (`wweia_food.csv` alone; the other two tables
need a join, which is six notebooks away). Chapter 7 is the chapter where a geometry
runs a grouped computation for you, so it wants a table that punishes you for letting
it. This one does, in three places. `meal_name` has 20 categories and no order, so
`geom_bar` draws them in storage order and the two smallest sit at the top. `kcal` is
so skewed that a plain histogram is a single bar: 23,132 of the 173,174 items have
exactly zero calories, because water, black coffee and diet soda are food items too,
and nearly half of everything filed under `Drink` is a zero. And `day_of_week` is an
integer, so `geom_boxplot` reads it as continuous and draws *one* box parked at x = 4
instead of seven, with no error, which is the chapter's cast-to-string lesson (7.4)
happening to you rather than being explained at you.

Notebook13 keeps the table, as the chapter pair allows, and the skew keeps paying. The
zeros that ruined notebook12's histogram are what makes `scale_x_log10()` a lesson rather
than a formality: a log axis cannot draw a zero, so it removes all 23,132 of them and
says so only in a warning. What it buys in exchange is a second hump, 20,135 items between
1 and 10 calories, which turn out to be brewed coffee, mustard, ketchup, hot sauce, and
lettuce "for use on a sandwich". The linear axis had them stacked in the first bin with
the water. The derived person-level table also gives the notebook a two-level split worth
coloring by (people who took most of their calories at home, 8,613 of them, against 3,311
who did not, and the second group reports 200 calories more), and `food_source` has 27
categories, which is what a color scale looks like when it dies.

The remark that earns the notebook its written question is in the meal names. Ten of
the 20 are Spanish (`Cena`, `Desayano`, `Almuerzo`, `Merienda`, ...), because the
interview was conducted in the participant's language and the label records the word
they used: roughly 90 percent of the rows carrying a Spanish label come from a
Spanish-language interview, and the survey misspells its own category (the word is
*desayuno*). A `group_by` on that column therefore splits dinner across `Dinner`,
`Supper` and `Cena`. The column looks like a property of the food and is partly a
property of the interview. Students cannot verify this yet, since it needs a join to
`wweia_demo.csv`, which is worth saying out loud in the answer as a promissory note
for notebooks 18 and 19.

Notebook14 takes the Shakespeare corpus, and it takes all four tables at once, which is the
one place in these notebooks where that is the right call rather than a lapse. The four files
are not four datasets. They are one corpus recorded at four nested grains: 37 plays, 1,126
character entries, 80,592 lines, 599,864 words. A chapter whose third tidy rule is "one
table, one unit of observation" wants a corpus that already obeys the rule, so that students
can see what obeying it looks like before they are asked to find a violation. Chapter 9
itself uses `countries.csv` and `countries_cellphone.csv`, so nothing collides.

Check the scope before planning anything, because it is tighter than it looks. Sections
9.1–9.4 are Setup, Introduction, Units of Observation, and Tidy Data, so notebook14
introduces **no new methods at all**: pivot, unpivot, and explode are 9.5–9.7 and belong to
notebook20. And because the class order splits chapter 9 around chapter 8, these students
have no joins either. Everything in the notebook is chapters 1–7 turned on a new question,
and the design problem is finding a corpus where the old tools uncover something that the
concepts alone would not.

Shakespeare does, in four places, all of them real:

- **The key that is not a key.** `character_id` looks like the primary key of the characters
  table and is not: 1,126 rows, 1,066 distinct ids. `Bardolph_1H4` has four rows, because
  Bardolph turns up in four plays, and the id names the play where a character *first*
  appears rather than the play the row is about. The unit is *character × play*. Thirty-nine
  characters cross plays and account for the sixty extra rows. This is the whole notebook in
  one column: the unit of observation is a claim, `.n_unique()` is the test, and the test
  fails.
- **What the broken key then does.** Grouping the lines by `character_id` alone pools a
  character across every play they appear in, and Polars does not complain. Hamlet drops from
  second to fifth. `Antony_JC` shows 1,148 lines, which is *Antony and Cleopatra* plus
  *Julius Caesar*. Best of all, `HenryIV_1H4` shows 1,044 and the largest block of them, 411,
  is in *Richard II*, where he is Bolingbroke and not yet king. A wrong grain does not raise
  an error. It returns a leaderboard.
- **A variable packed into a cell.** `line_number` is a string, `"3.1.64"`, holding act,
  scene, and line. Act and scene already have honest `i64` columns; the number that actually
  orders the speeches exists only inside that string. Sorting a scene by it gives 3.1.1,
  3.1.10, 3.1.100, which is the first tidy rule failing where a student can watch it happen.
  They cannot repair it, since prying the parts out needs `str.split` and `explode`, and that
  is the point.
- **A cell holding a set.** `character_id` in the lines table sometimes holds several ids
  joined with `#`, which is how the Folger records characters speaking in unison. Macbeth's
  personae lists the Weïrd Sisters as a single row; the lines table has three separate witches
  *and* a fourth cell containing all three of them, 21 lines, including the "Double, double
  toil and trouble" refrain. 177 lines in the corpus do this, in 75 distinct combinations, and
  the worst of them packs ten characters into one cell, drunk on Pompey's galley at *Ant*
  2.7.138. This is the list column of 9.7 turning up in the wild, before the tool for it
  exists.

One more, a warning rather than a lesson: `line_type` is `"verse"` on all 80,592 rows,
including every scene of prose the man ever wrote. A column with one distinct value is not a
variable, it sails through a tidy inspection untouched, and no rule about shape can catch it.
It earns a question, because the tidy rules are about shape and students will otherwise leave
believing that shape is all there is.

Notebook14 is built to leave IOUs, and **notebook20 should collect them on the same corpus**,
which the chapter-pair rule allows. The packed `line_number`, the `#` cells, and the closing
question (one row per play and one column per act, which is a pivot they cannot write yet) are
all set up to be paid off by 9.5–9.8. Labeling the bars of notebook14's closing chart with
real character names needs `name` from another table, which is a join, so that one is an IOU
for notebooks 18 and 19.

Notebook15 takes the Paris Métro stops, 371 rows and seven columns, and it is the rare case
where the *file* is the subject rather than the thing you look through at a subject. Sections
10.1–10.5 are Introduction, What Tables, What Variables, What Variable Names, and Storing Data
in Spreadsheets, so the class is entirely about decisions made before any data exists, and it
introduces no new methods either. Two conceptual notebooks in a row is a real risk, and the
way out is that notebook14 asked "what is a row?" of a corpus that was stored *correctly*,
while notebook15 asks the same question of a file that was not. The chapter's rules are all
stated as advice for when you collect. Students almost never collect. So point the rules
backwards: take a published file, work out which rule its author broke, and make them pay the
bill.

This file breaks four of them and pays for each, which is why it survived the search:

- **A column that is a fact about the group.** `line_color` never varies within a line:
  fourteen facts written down 371 times. The chapter's "respect the unit of observation" rule
  in its purest form, and `.unique(subset=c.line)` builds the two-row-wide `lines` table that
  should have held it.
- **The same test, giving the opposite answer.** This is the best thing in the notebook, and
  it is worth protecting in any rewrite. `lon` and `lat` *look* like facts about the station,
  so the rule should condemn them too, and it does not: Châtelet has five rows and five
  different longitudes, and 49 of the 53 multi-line stations behave the same way. The
  coordinates are *platform* positions, not station positions, so they are a fact about
  station × line, which is the unit, so they belong. Converted to metres the spread runs to a
  median of 43 m and a maximum of 312 m at Montparnasse-Bienvenüe, then Gare de Lyon at 268 and
  Châtelet at 207, which is a ranking any Parisian can confirm by having walked it. The lesson
  is that "respect the unit of observation" is a rule you *run* (`group_by` and `n_unique`),
  not a rule you eyeball, and here the counting overturns the thinking.
- **A stored derived column.** `lon_end` and `lat_end` are the *next* stop's coordinates,
  which is to say a copy of another row. `.shift(-1).over(c.line)` reproduces 352 of them
  exactly, 13 more are missing in both, and 6 disagree. Those 6 are the payoff: they are the
  branches and the seams (line 7's Mairie d'Ivry branch, line 13 forking at a station actually
  named La Fourche, line 4's terminus stored first so the chain wraps, and line 1 skipping
  Porte Maillot and stranding it). The order of stops along a route is real information, this
  file has no column for it, it survives only as *row order*, and the author smuggled it into
  duplicate coordinates. The duplication is a workaround for a missing variable rather than
  laziness, and saying so is what keeps the notebook from being a scolding.
- **A type that decided what could exist.** `line` is an `i64`. Paris has sixteen métro lines;
  this file has fourteen. "3bis" and "7bis" are not integers, and the seven stations unique to
  those two lines (Pelleport, Saint-Fargeau, Bolivar, Buttes Chaumont, Botzaris,
  Pré-Saint-Gervais, Danube) return zero rows. "Prefer numeric" is good advice about
  quantities, and a line number is not a quantity. This closes the notebook.

Two more things the file gives for free. The `"NA"` placeholders in `lon_end`/`lat_end` (18 of
them, all termini) load the columns as `str`, which is chapter 3's lesson arriving as a
*storage* decision rather than an accident. And the station names have had every accent
stripped ("Reaumur Sebastopol", "Franklin D.Roosevelt" with the space missing), so the only
identifier of a station in the whole file is a mangled display name, which is what motivates
the synthetic key in the closing schema.

The notebook has one plot and it was rendered before being described. The `geom_point` map,
colored by `scale_color_manual` with the real RATP palette pulled from the `lines` table, is a
nice joke on question 3: the column we spent a question calling redundant is the column that
draws the map, and the split-out table is a perfectly convenient place to keep it.

A second plot was drafted and **cut**, and the reason is worth recording so it does not get
re-added. Swapping `geom_point` for `geom_line` draws a picket fence, because `geom_line`
connects in x-order rather than row order: lines 1, 8, and 9 come out looking almost right
(they run east to west, so route order and longitude order nearly agree) while lines 4, 7, 13,
and 14 come out as vertical spikes. It is a pretty demonstration that the route order is not in
any column. It is also a whole question spent on a plot that fails for a reason question 8 has
already established in the data, and the notebook does not need the second telling. Eleven
questions was one too many; ten is the notebook.

The closing written question asks for the three-table schema (`lines`, `stations`, `stops`,
the last one carrying the branch and route-position columns the file never had), and it lands
on the trade rather than a verdict: the file flattened everything into one table so that no
join would ever be needed, and it paid with a color repeated 371 times, a coordinate written
twice, an ordering that survives only until someone sorts, and seven stations that do not
exist. Reassembling the three tables is a join, which is an IOU for notebooks 18 and 19.

Notebook17 takes the FSA-OWI color photographs, and it is the one notebook so far that had to
**build its own data file**. Read the next few paragraphs before touching it, because the
reasoning matters more than the result.

Sections 10.6–10.10 are Reading Imperfect Files, Data Dictionary, Special Considerations,
Worked Example, and Extensions. Only 10.6 introduces any method, and what it introduces is
`pl.read_csv()`'s arguments: `separator`, `encoding`, `skip_rows`, `null_values`,
`schema_overrides`. So the class needs a file that *needs* them. Nothing in `data/` does. A
sweep of every CSV in the directory turns up placeholder `"NA"` strings in a dozen files and
nothing else: no semicolon-delimited file, no non-UTF-8 file, no file with junk above the
header. The only imperfect file in the repo is `cities_messy.csv`, which is chapter 3's own
and which 10.6 explicitly revisits, so it is out under the avoid-the-chapter's-dataset rule.

`data/fsac_export.csv` is therefore constructed, by `scripts` you will not find because the
builder was a throwaway. **It changes no data.** It is the same 500 rows of `data/fsac.csv`,
rewritten in the format a 2003-era archive export tool would have produced:

- two preamble lines (a title and an export stamp) above the header, so `skip_rows=2`;
- a pipe separator, so `separator="|"`. This one is not arbitrary and the notebook says why:
  495 of the 500 captions contain a comma and 54 contain a semicolon, and none contains a
  pipe, so a pipe is the character the text cannot collide with;
- windows-1252 encoding, so `encoding="windows-1252"`. The non-ASCII characters are real: the
  Library of Congress escapes apostrophes and quotation marks in its captions as `&#39;` and
  `&quot;`, and the export decodes them back to the typographic `’ “ ”` that the archivist
  actually typed. It leaves `&amp;` undecoded in 45 captions, which is what a half-finished
  unescaping looks like and is extremely common in the wild.

Nothing else was touched, and the builder asserted it: every column except `caption` compares
equal to `fsac.csv` after a correct read. If the file ever needs rebuilding, that assertion is
the specification.

The one argument the notebook does not call is `schema_overrides`, because nothing in this
file needs it and inventing a reason would have been a lie. It gets its paragraph anyway, in
the answer to question 8, as `null_values`' sibling (both prevent damage at read time rather
than repairing it after) and it is paid for out of the students' own history: notebook15
closed on the Métro's `line` column being an `i64` that could not hold `3bis`, and
`schema_overrides={"line": pl.String}` is the version of that file where those seven stations
exist. Chapter 3 makes the same promise (*"we cover the options for reading imperfect files in
@sec-collect"*) and this is where it comes due.

What earned FSA-OWI the notebook is that everything *after* 10.6 is native to it, and real:

- **A key that fails, and a file name that catches it.** 500 rows, 499 call numbers. The
  duplicated row is `media/fsac/1a35434v.jpg` carrying `LC-DIG-fsac-1a35424`, and printing its
  neighbors is the whole lesson: `1a35430` through `1a35433` and `1a35438`/`1a35439` all match
  their filenames digit for digit, so you can say which of the two fields is wrong, which you
  almost never can. This is 10.8's multimedia rule (put the file name in a column) and 10.8's
  key rule colliding: storing the path gave the photograph a second, independent identity, and
  that is the only reason the typo is visible.
- **A date that cannot be ISO 8601.** `year` and `month`, no day, because the archive does not
  know the day. The chapter offers two options and this file takes the separate-columns one
  because the other would have forced it to invent 500 days. The notebook invents one anyway
  (`pl.date(c.year, c.month, 1)`) to get a plottable axis, and says out loud that this is fine
  in a chart and a lie in a file.
- **A missing value that `null_count()` cannot see.** DC is not in a county, and the five
  Washington rows say `US.DC.001`, a geocoder's internal code parked in a column of English
  county names. `null_count()` reports zero nulls across the whole table. `null_values=["US.DC.001"]`
  makes it report five.
- **The best thing in the file: `county`.** Every one of the 495 non-null values is exactly two
  words long, which is not a fact about American county names. It is a fact about whatever
  script wrote the column. Los Angeles County became `Los County` (40 photographs) and San
  Bernardino County became `San County` (11), while `Shasta County` came through intact because
  its name was already two words. All three sit in the same ten-row California table, which is
  why the notebook prints exactly that. And note what it does to the obvious audit: `Los County`
  *ends in the word County*, has no nulls, and groups cleanly. The format check passes and the
  data is false, which is the argument for a FIPS code and not an aesthetic one.

Two things to protect in any rewrite. The first is the encoding sequence in questions 1 through
4, which is a deliberate failure in three acts: the naive read raises, `utf8-lossy` makes the
error go away and silently corrupts 98 captions, and only `windows-1252` decodes them. That is
the "a fix that silences the symptom is not a fix that gives the right answer" lesson from
section 5 of this document, arriving as something the student does with their own hands. The
second is question 10's coordinate test, which is notebook15's Châtelet moment run again and
coming out **the other way**: `lon`/`lat` never vary within a city (0 of 108), so here they are
city centroids and do *not* belong on a photograph, where in Paris they were platform positions
and did belong on a stop. Same test, opposite verdict, and it is the clearest way to say that
the test tells you what a column cannot mean rather than what it does mean.

The notebook does not open an image, though `filepath` points at real files in `media/fsac/`.
Colab would need 500 downloads for a chapter that is not about images. That is chapter 17's job
and the notebook says so.

Ten questions. The closing written question is the data dictionary, and it lands on the
asymmetry: every line of it took a query to find and one sentence to write down.

Notebook18 takes the RVA flights, all five tables, which is the second place in these notebooks
where a whole corpus is the right unit rather than a lapse. A joining chapter needs tables that
key to each other, and it needs at least one key that *fails*, because a notebook in which every
join works is a notebook about syntax. Chapter 8 uses `countries.csv` and `countries_borders.csv`,
so nothing collides.

Check the scope first: 8.1–8.6 are Setup, Introduction, Primary and Foreign Keys, Joining by
Relation, Join Examples, and Filtering Joins. So notebook18 gets keys, `.join()`, `on=`,
`left_on=`/`right_on=`, `how=`, `suffix=`, a list-valued `on=`, and semi/anti. It does **not** get
the fan-out demonstration of 8.7 (a duplicated right-hand key silently multiplying rows), the
conditional joins of 8.8, or the agg-then-join-versus-`.over()` comparison of 8.9. All three belong
to notebook19, which should stay on this corpus, since `weather` is an hourly time series and the
flights are timestamped, which is what `join_asof` was built for. Note that the notebook still runs
the key check (`.n_unique() == len()`) before every join: that is 8.7's *tool*, but the students have
had it since notebook14, and running it as a precaution is not the same as showing them the fan-out.

Three things earned this corpus the notebook, and all three are real:

- **An inner join that deletes an airline.** Joining `rva` to `plane` on `tailnum` returns 24,346 of
  the 24,808 flights and 13 of the 14 carriers. Every one of Allegiant's 396 flights is gone, with no
  error and no warning, and the mean-seats-per-carrier summary that comes out looks perfectly sane.
  The anti-join names the culprit in one line: 462 unmatched rows, 396 of them `G4`. The rest of the
  story is better than the setup. Allegiant's tail numbers are stored *without* the leading `N`
  (`330NV`, not `N330NV`) in 395 of their 396 rows, which looks exactly like the cause and is not:
  prepending the `N` and joining again matches **zero** rows. The registry has no Allegiant aircraft
  under any spelling. A semi-join explains why that is odd, since all 3,120 rows of `plane` flew out
  of Richmond, so the table is not a national registry with gaps but a table derived from this very
  dataset, and Allegiant fell out of whatever built it. This is section 5's rule again, arriving in a
  student's hands: **a fix that explains the symptom is not the same as a fix that works.** The cost
  is also larger than one airline. `G4` is the only carrier flying to SFB, PIE, BNA and SRQ, so the
  inner join removes four of the 22 destinations from the map, and the map still looks fine. (The 13
  `null` tail numbers are the cancelled flights, and a `null` key matches nothing, so cancellations
  quietly leave through the same door.)
- **The best thing in the corpus: two tables on different clocks.** `rva` and `weather` both have a
  `time_hour` column. Same name, same format, same type, and `dataset_description.qmd` explicitly
  recommends it ("allows this data to be precisely joined with flight departures"). It is the wrong
  key. In `weather`, `time_hour` is a true UTC stamp, so local hour 0 on 1 January reads
  `2019-01-01T05:00:00Z`. In `rva`, it is the *local* hour with a `Z` pasted on the end, so the 5:50am
  departure also reads `2019-01-01T05:00:00Z`. Joining on it hands every flight the weather from five
  hours earlier: our 5:50am flight gets the 1.0-mile visibility of the midnight fog, when the actual
  visibility at 5am was 10.0. 4,835 of the 24,808 rows come back with a different visibility depending
  on whether you join on `time_hour` or on `[year, month, day, hour]`. The four-column key is the
  correct one (flights' `hour` runs 5 to 22 and peaks at 6am, so it is plainly local; read as UTC it
  would put the first commercial departure at 12:50am), and it finds 1,254 low-visibility flights at a
  15.1-minute mean delay against the wrong key's 1,173 at 16.4. **Both keys support the same
  conclusion**, which is the entire point and must not be softened in a rewrite: the join did not fail,
  the number was plausible, the finding survived, and the analysis was still built on the wrong hour.
  The anti-join leaves a fingerprint for anyone who checks: 57 flights match no weather at all under
  `time_hour`, 50 of them on 31 December (the feed stops on the 30th) and 7 at 6am on 3 November, the
  morning the clocks went back, where the weather's UTC index has no `06:00:00Z` and the flights table,
  keeping local time, insists that there is one.
- **A join that matches everything and returns nothing.** `weather` has 8,735 rows and joins cleanly,
  and `temp`, `dewp` and `humid` are `null` in 8,678 of them, `precip` in 8,467. Only wind and
  visibility were reliably recorded, which is why the notebook asks about visibility. Had it asked
  about temperature, the join would have matched every row it was asked to match and handed back a
  column of nulls. It closes on this, because it is the quiet version of the same lesson: a successful
  join tells you the keys lined up and nothing else.

The notebook has one plot, the 22 destinations drawn from `airport`'s coordinates, sized by traffic
and colored by mean arrival delay. It was rendered before it was described, and the first draft's
description was wrong in the usual way: it said the New York airports were the yellow dots, and they
are green. The latest arrivals are Dulles and O'Hare, plus two small dots in Florida. What is worth
protecting in the answer is Tampa and St Petersburg, fifteen miles apart at the left edge of the
Florida cluster, the darkest dot on the entire map (7.5 minutes early) sitting next to one of the
brightest (15.3 late), and served by two airlines that fly to neither of the other's airport. One of
those airlines is Allegiant, which is a nice piece of foreshadowing three questions before the
inner join deletes it.

Ten questions. Questions 7 and 10 are the written ones, and they have the same shape: a few lines of
code that settle a question, then a paragraph saying what the code proves. The closing pair (two keys
that disagree, then the two printed rows that adjudicate between them) is the notebook, and everything
before it is the equipment.

Notebook19 keeps the flights corpus, as the chapter pair allows and as notebook18 predicted it would.
Sections 8.7–8.9 are Diagnosing Bad Joins, Conditional Joins, and Attaching a Group Summary, so the
class gets the fan-out, `.join_asof()`, `.join_where()`, and the `.over()`-against-agg-then-join
comparison. Every one of the three has a home in this corpus that is real rather than staged, which
is what kept the notebook on the flights rather than moving on:

- **The fan-out, and the summary that survives it.** This is the best thing in the notebook and the
  thing to protect. Joining `rva` to `weather` on `[year, month, day]` instead of the four-column key
  is a *plausible* thing to want (each flight should know what the weather was like that day), and it
  returns 594,122 rows from a 24,808-row table, because each date has 24 hours behind it. Nothing
  errors. Then comes the part that makes it a lesson: the mean departure delay per carrier computed on
  the fanned table is **the same number** as the correct one, to three significant figures (SkyWest
  13.55 in both, Delta 1.66 in both, ExpressJet 23.02 against 23.06). It has to be, since every flight
  was copied the same 24 times and a uniform reweighting does not move a mean. The tiny wobbles are the
  days with 23 hours of weather. So the notebook can say the thing that is hard to say any other way:
  *the table was wrong by half a million rows and the summary was right*, and the only reason you know
  is that you printed `n`. The damage shows up on the very next question, because counting flights with
  visibility under five miles on the fanned table gives 26,097 against a true 1,254. The mean delay never
  touched a `weather` column and so the duplication cancelled; the visibility filter is *about* a
  `weather` column and so it does not. The fanned table is not garbage either, and the notebook says so:
  it is one row per flight-hour, a perfectly good unit, just not the one that was asked for.
- **The repair is 8.9's shape arriving early, which is fine.** Collapsing `weather` to one row per day
  and *then* joining gives 24,758 rows and 5,945 flights that flew on a day with at least one hour under
  five miles. Group-then-join is not new (notebook18's question 3 does it), so this does not spend 8.9's
  material; what 8.9 gets at the end is the *comparison* and, more importantly, the structural claim about
  when `.over()` is not available at all. Note the 24,758 against 24,808: the 50 missing are last class's
  December 31 flights, since the weather feed stops on the 30th, so the seam is the same one and students
  meet it twice.
- **`join_asof` earns its place on the emptiest column in the corpus.** `temp` is recorded 57 times in
  8,735 rows, so an equi-join on the hour would match almost nothing, which is exactly the situation the
  method exists for. It also loads as `str`, because nearly every value is missing and Polars infers from
  a window of nulls, so the question needs a `.cast(pl.Float64, strict=False)` before anything else can
  happen: chapter 3 turning up inside a chapter 8 problem, which is where it usually turns up. The asof
  join then hands a temperature to all 24,808 flights and reports a mean of 61.2°F, which is a completely
  believable annual mean for Richmond and is built on nothing. **`.join_asof()` cannot fail**, and that is
  the entire lesson: it always returns one row per left row, so the row count, which was the thing that
  caught the fan-out three questions earlier, is now useless. `coalesce=False` keeps the matched row's own
  stamp so the distance can be measured, and the distance is grotesque: a median staleness of 394 hours
  (sixteen days), only 266 flights matched within an hour, just under 16,000 matched to a reading over a
  week old, and 3,493 with no match at all because they flew before the first reading on February 25. The
  row to print is the worst one, and it is worth protecting: a flight leaving at 2:05pm on August 21 is
  handed the temperature from 5am on June 22, sixty days stale, and told it was 66.2°F. In Richmond. In
  August. In the afternoon. The rule the notebook lands on is that a join which always succeeds has told
  you nothing by succeeding, so after any asof join you compute the gap and look at it.
- **`join_where` collects an IOU from notebook18.** Last class's map had a remark about two dots almost
  on top of each other in Florida (Tampa and St Petersburg, fifteen miles apart, no airline flying to
  both). Notebook19 finds every such pair without a picture: semi-join `airport` down to the 22 real
  destinations, then self-join it with `c.faa < c.faa_right` and a one-degree box on `lat` and `lon`. Eight
  pairs come back and all eight are real: the three New York airports account for three of them, Fort
  Lauderdale pairs with Miami, Orlando with Orlando Sanford, and the Tampa Bay trio (PIE/TPA, PIE/SRQ,
  SRQ/TPA) gives the last three. The self-join is the new idea, and `c.faa < c.faa_right` is doing two jobs
  worth naming out loud: it stops an airport pairing with itself and it keeps only one of each symmetric
  pair.
- **And the pairs turn out to be a business model.** Grouping the five Tampa/Orlando airports by carrier
  splits them perfectly: Orlando International has JetBlue, Spirit and Southwest, Tampa International has
  Southwest, and St Petersburg, Orlando Sanford and Sarasota have Allegiant and nobody else. Allegiant flew
  to exactly four places from Richmond in 2019 and three of them are on that list (the fourth is Nashville).
  So the near-duplicate airports are a low-cost carrier declining to buy a gate at the big field and flying
  to the cheap one fifteen miles away. This is also the airline that silently vanished from last class's
  inner join, which makes the callback do double duty.

The closing plot is a join between **two aggregates**, one per day from each table, and it is where the
notebook makes its structural point about 8.9. `.over()` can only group rows that are already in the table,
so the mean visibility of a day is a summary no expression written over `rva` can reach; it has to be an
aggregate and a join. A join is not a tidier `.over()`, it is the only option once the group lives elsewhere.

**Render the plot before describing it, and note what it does to the story.** It is a mild downward slope
(correlation -0.168) over a solid vertical wall of points at exactly ten miles of visibility, spanning
delays from five minutes early to forty minutes late. The worst day of the year (July 26, mean delay 41.9
minutes) had perfect visibility all day. Last class's hourly join found a real effect, since flights taking
off in fog leave 15.1 minutes late against 10.0 for everything else; this plot is built from the same two
tables and the effect has mostly evaporated, because averaging a day of weather into one number averages the
fog away with it. Nothing was joined incorrectly. The keys were unique, the row count was right, and the
grain was wrong. That is the note to end a joining unit on, and it is the reason the plot stayed in.

Ten questions. The written ones are 3, 7, and 10.

Notebook20 goes back to Shakespeare, which notebook14 said it should and which the chapter-pair
rule allows. Sections 9.5–9.8 are Pivot and Unpivot, Pivoting for plotnine, Expand List Columns,
and Round Trips Versus Aggregation, so the class gets `.pivot()`, `.unpivot()`, `.explode()`, and
the one-way-street argument about aggregation. It uses three of the four tables (`word` is not
needed) and it has joins now, since chapter 8 sits between the two halves of chapter 9 in the class
order, which is what lets it settle debts notebook14 could only name.

The whole notebook is the three IOUs notebook14 wrote, collected in order:

- **The packed cell that held a set.** The `#`-joined `character_id` values are what `.explode()`
  was built for. `c.character_id.str.split(" #")` and `.explode()` take the corpus from 80,592 rows
  to 80,968 and turn *Macbeth*'s four witch-shaped speakers into three: the phantom fourth witch
  with 21 lines disappears and the real three go from 59/25/24 to 80/45/46. Macbeth's distinct
  speakers drop from 49 to 44, and the 49 was never a number about the play.
- **The packed cell that held a record, and why explode is the wrong tool for it.** This is the best
  teaching moment in the notebook and it should survive any rewrite. Exploding `line_number`
  ("3.1.64") gives three rows per line and is *worse than the disease*, because the cell holds one
  value each of three different variables rather than three values of one. The repair is explode
  *then pivot*: number the exploded pieces within each line, then pivot the position back out into
  three columns. So the two halves of the chapter turn out to be one tool, and the distinction the
  chapter never quite states (a set versus a record) is the thing that decides which shape you need.
- **The pivot itself**, which is question 1, and which is the table notebook14 signed off asking for:
  one row per play, one column per act.

Numbering the exploded pieces needs `.cum_count()`, which is **the one method in this notebook the
students have not seen**, and it is worth being honest about why. `pl.lit(1).cum_sum()` does not work
(the literal is a scalar and does not broadcast to the group), `.list.get()` contradicts the chapter,
which explicitly steers away from list methods, and every other route is an idiom nobody should copy.
`.cum_count()` is one token from notebook11's `.cum_sum()`, so the notebook introduces it in a single
sentence in the question prompt. If a cleaner in-scope route turns up, take it.

**What the notebook actually finds is not in the chapter, and it is the reason the notebook exists.**
Once `line_number` is unpacked, the third piece is an integer that orders the lines of a scene, and a
scene numbers from 1, so the highest number in a scene is how many lines that scene has. Compare that
with how many rows the table holds and the corpus confesses: 80,592 lines recorded against 101,886
numbered, and only 123 of the 688 scenes complete. **The prose is missing.** All of it. The Porter has
a row in `char` and zero lines in `line`, Macbeth 2.3 starts at line 22, Macbeth 5.1 starts at line 75
so "Out, damned spot" is not in the corpus at all, and Falstaff has *eight* lines in *1 Henry IV*.

Which means `line_type`, the column notebook14 dismissed as a broken label because it says `verse` on
all 80,592 rows, was telling the truth. The table holds the verse and nothing else. A filter had
already been run, it was recorded honestly in a column with one value, and it took a pivot, an
explode, and another pivot before anyone could read it. That is the ending, and it is a much better
one than the chapter's own.

The finding is falsifiable, which is what makes it teachable, and question 9 is where it gets
falsified. Verse share per play, plotted: *The Merry Wives of Windsor* keeps 30 percent and is the most
prose-heavy play in the canon, then *Twelfth Night*, *Much Ado*, *All's Well*, *1 Henry IV*, *As You
Like It*, which is the prose comedies and the Falstaff plays in almost the order a scholar would give
them. Sorted the other way it is *1 Henry VI*, *King John*, *3 Henry VI*, *Richard II*, all at 97
percent or better, and *Richard II* is famous for being written entirely in verse. Two things to keep
honest here: the share is approximate, since the all-verse plays land a point or two short of 100 and
those stray missing lines are *not* prose (in *Richard II* 5.3 the gaps are isolated singletons), and
no reshape recovers the prose, which is the difference between a table in the wrong shape and a table
with a hole in it.

The two earlier plots are also load-bearing and were both rendered before being described, which
caught a wrong first draft. The four-tragedies chart in question 4 (unpivot, then one line per play
across the acts) was drafted from memory as "Hamlet is enormous in act 2" and the render says the
opposite: *Hamlet* has 897 lines in act 1 and 423 in act 2, a fall of more than half, in the act with
Polonius, the players, and Rosencrantz and Guildenstern. That collapse is the missing prose, four
questions before the notebook knows it, so the question now flags the anomaly and refuses to explain
it. Same with question 6's twelve-biggest-parts chart, notebook14's closing figure redone with real
names: the name to notice is the one that is *absent*, since Falstaff does not make the list. Both
plots are set up as clues and both are cashed in question 8.

Question 6 also collects an accidental third debt. Joining the top twelve to `char` on `character_id`
alone returns **seventeen** rows, because `RichardIII_R3` has three rows in `char` (Richard of
Gloucester is in both parts of *Henry VI* before he gets his own play). That is notebook19's fan-out,
caused by notebook14's broken key, showing up in notebook20 as a bug. The compound key fixes it. It
was not planned and it is the best argument in this document for the tool ledger.

Ten questions. Question 10 is the written one, and it lands 9.8 where the corpus has already proved
it: pivots are reversible and aggregation is not, so store long. And then the twist, which is that
this corpus stored long and *still* lost the prose, because somebody ran a filter upstream and only
the shape of the data remembers.

**Notebook14 needs a correction, and it came out of drafting this one.** Its question 8 answer says
every line is labeled `verse` "including the gravediggers, including Falstaff, including every scene
of prose the man ever wrote," which is false: those scenes are not in the table at all, mislabeled or
otherwise. The label is accurate and the rows are gone. Its question 9 chart is also the twelve biggest
*verse* parts rather than the twelve biggest parts. Neither claim raises an error and both were written
from plausibility, which is the same trap this document already names three times. Fix notebook14 to say
that a column with one value is a variable that cannot vary *and may be a filter somebody already ran*,
and let notebook20 pay it off.

## 3. Write the file

Filename `notebookNN.qmd` at the repo root, next to
`notebook_example_format.qmd`, which is the canonical format. Header is
`## NotebookNN`, then `### Setup`, then `### Questions`.

The setup blocks are fixed boilerplate — copy them from an existing notebook and
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

The load cell may quietly clean the data with methods the students have not met
yet — it is given to them, not written by them. Use this to remove problems the
chapter has no tools for. Notebooks 03 and 04 `.select()` a workable subset of
columns and drop rows missing the core numeric fields, because Polars sorts
nulls to the *top* of a `descending=True` sort and a notebook on sorting should
not open with a screen of blanks. Leave in the mess the chapter is *about*.

Open `### Questions` with a short paragraph introducing the dataset: what a row
is, what the columns mean, any unit that is not obvious. Then say results should
be printed, not saved, unless a question says otherwise.

## 4. Shape the questions

Ten to twelve numbered questions. Thirteen was judged a little long.

The arc runs from a one-method question to a short pipeline: each question adds
roughly one idea, and the later ones should be answerable by copying the previous
answer and changing a line. Follow the chapter's own order of presentation, so a
student who is stuck can find the relevant paragraph by scanning forward.

Write each answer as a chain in the book's house style: parentheses on their own
lines, one method per line, four-space indent, `c.` column references. The
answers we write are the answer key, so they should be the code we want copied.

Some things worth including:

- **A written question or two.** Not everything is code. "Why does this filter
  miss 26 films?" (the `"Japan|France"` encoding) and "which three columns have
  a type you would not expect?" make students look at the data. Give the answer
  in bold as **Answer**: followed by the explanation.
- **A deliberate failure.** Notebook03 asks for the top Metacritic films the
  obvious way, gets nulls sorted to the top, and fixes it in the next question.
  Showing the trap beats warning about it.
- **Old tools inside new questions.** Scan the tool ledger above before writing,
  and build the later questions so they need earlier material to answer: a
  `.filter()` to narrow the rows before the new method runs, a `.sort()` and
  `.head()` to show only the interesting end of the result, a `.cast()` because
  the column arrived as text. The new method is the point of the question, but it
  should rarely be the only thing in the chain.
- **A remark about the data itself** where the data earns it. Criterion budgets
  are reported in local currency, so the most "profitable" films are the ones
  denominated in yen — a column can be clean and still be measuring several
  different things. These asides are the difference between an exercise and a
  data science course.

Prose should be plain and short. Address the student directly, explain what a
result means when it is surprising, and do not pad.

## 5. Verify before handing it over

Every code block must run. Extract and execute them in order:

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

Then check every number that appears in the prose against the data. If a question
says "there should be 172 of them," run it and count. Row counts change when the
setup cell cleans the data, and a wrong number in the answer key wastes a room
full of students' time.

Run the chapter's claims too, rather than writing an answer from them. Two errors
in Chapter 5 survived to the notebook-drafting stage and were caught only by
executing the code. `.n_unique()` does not skip missing values the way `.count()`
does: Polars counts `null` as one more distinct value, so a column with three
labels and some blanks returns 4. And the section on counting demonstrated the
`pl.len()` versus `.count()` gap on `hdi`, which is complete for all 135 countries,
so the printed table showed no gap while the prose described one. `gini` is the
column in `countries.csv` with holes in it. Both are fixed now, but the lesson
generalizes: a claim about missing data is only as good as the column it is
demonstrated on, and columns get swapped.

Check the top row of every sorted result against the raw rows it came from, not just
against the error you were trying to remove. Notebook10 drafted the repair for the
divide-by-zero growth rates as a `.filter(c.population > 0)` in front of the
`.shift()`, which does remove every `NaN` and `inf` and returns a clean, plausible
table with Mesquite, Texas at the top. Printing Mesquite's own censuses showed the
number was comparing 1960 against 1900, because dropping rows had redefined what
"the row above" meant. The corrected chain became a question in its own right, and
the notebook is better for it, but the point stands: **a fix that silences the
symptom is not the same as a fix that gives the right answer**, and only the raw
rows behind the winning row can tell the two apart.

Chapter 7 turned up three more, all in the sections notebook13 covers, and all of them
survived because the offending blocks are marked `eval: false` and so had never run. Two
are now fixed in the chapter and one is still open:

- **Open.** 7.7 calls `breaks_width(0.05)` with no import. It is not in `plotnine`; it
  lives in `mizani.breaks`. As written the block raises `NameError`. The block is
  `eval: false`, so nothing breaks at render time, but a student who copies it gets an
  error. Notebook13 sidesteps it by passing `breaks=` an explicit list.
- **Fixed.** 7.8 said `facet_wrap` takes a `space` option set to `fixed`, `free_x`,
  `free_y`, or `free`. The argument is `scales`; passing `space=` raises `TypeError`. The
  confusion is understandable, since `facet_grid` really does take both, where `scales`
  sets the axis ranges and `space` sets the panel sizes. The section now says so.
- **Fixed.** 7.7 said `scale_color_cmap_d()` replaces "the default rainbow" with
  purple-to-yellow. It does not, because purple-to-yellow already *is* the default here:
  `funs.py` casts every string column to an ordered `pl.Enum`, plotnine gives *ordered*
  categories the viridis scale without being asked, and the two plots come out
  byte-identical. (The rainbow the sentence describes, `scale_color_hue`, is what plain
  unordered pandas data gets.) Rather than change the `Enum` cast, which is what makes
  category order follow the data, the section now says the default is viridis, names the
  scale that produces it, and demonstrates `scale_color_brewer(type="qual", palette=2)`
  as a change you can actually see. Any future claim that a scale "changes" the colors
  should be rendered twice and diffed before it goes in.

One more, not an error but an omission with teeth: `limits=` on a continuous scale does
not zoom, it *deletes* the rows outside the range, and any stat then refits on the
survivors. In notebook13 that moves the fitted line from 0.34 to 0.41 calories per gram
and drops 1,076 people, with only a `Removed 1076 rows` warning to show for it.
`coord_cartesian(xlim=, ylim=)` is the crop. The chapter should probably say this where it
introduces `limits`.

Chapter 10 turned up one more, in 10.6, and it is the good kind of wrong. The section says that
"reading a file with the wrong encoding usually produces garbled characters rather than an
outright error, so this one is easy to miss." In Polars it does not. The default is
`encoding="utf8"`, and windows-1252 bytes make it raise `ComputeError: invalid utf-8 sequence`,
loudly, on the first bad byte. The garbling the sentence describes is what you get from
`encoding="utf8-lossy"`, which is the *fix* a stuck student reaches for. (The chapter's `JosÃ©`
example is the other direction: UTF-8 bytes read as latin-1.) The real behavior is better
material than the claimed behavior, and notebook17 is built on it, so the fix is to correct the
sentence rather than to work around it. Verified on Polars 1.42.1.

And a small counting trap from the same notebook, worth the warning because it produced a
confident wrong number in a first draft. Asking how many captions contain a semicolon returned
129, which went straight into the prose. It is 54. The other 75 were `&#39;` and `&quot;`, both
of which end in a semicolon. When a column contains escaped text, a `str.contains` on
punctuation is counting the escaping too.

Notebook18 adds a rule for joins specifically, and it cost an afternoon to find. **A shared column
name is not evidence that two columns are the same variable.** `rva.time_hour` and `weather.time_hour`
have the same name, the same string format, the same type, they match on 24,751 rows, and
`dataset_description.qmd` recommends the join in as many words. They are five hours apart, because one
table converted to UTC and the other pasted a `Z` onto a local timestamp. Nothing about the join
complains, and the analysis it supports comes out plausible and even survives the error. The only way
this surfaced was printing one flight next to the weather rows around it and reading the clock. So
before joining on a column, check what a single value *means* on both sides, and be most suspicious of
the key the documentation is proudest of. Timestamps, currencies, and anything with units are where
this hides.

The same afternoon produced a smaller warning about being clever. The Allegiant tail numbers in the
flights table are missing their leading `N`, which is a real anomaly, and it is *not* why the join
fails. Prepending the `N` matches zero rows. It went into a draft as the explanation before it was
run, because it was too tidy to doubt. **Run the fix you are about to describe, especially when it is
elegant.**

For a notebook with plots in it, running the blocks is not verification. A plot
that builds without error can still be a black smear, and the prose underneath it
is a claim about what a student will see. Save each plot with `.save()` and look
at the image before you describe it. Every graphics answer written from
imagination in notebooks 06 and 07 turned out to be wrong in some detail: the map
of all 25,112 storm observations is a solid mass rather than a legible coastline,
the wind ceiling above 40 degrees drops by 40 percent and not by half, and the
bars of a `geom_col` follow the row order of the data and not, as Chapter 4
currently claims, alphabetical order.

The picture also catches bugs that the table hides. Notebook11's closing figure was
first drafted with the `.filter()` for the six cities in front of the windowed share,
copying the shape of the chapter's own closing plot, where filtering first is
deliberate. Here it was not: the denominator quietly became the six chosen cities, and
the render showed New York sitting at exactly 100 percent from 1790 to 1830 with a
flat line no reader could miss. The same error in a printed table would have looked
like a column of plausible percentages.

Two smaller traps, both from notebook12. First, the descriptive claims are the ones
that rot: a draft said the four main meals were 77 percent of the items (they are 76)
and that the daily-calorie density peaked "a little below 2,000" (it peaks at 1,596).
Neither would raise an error and both were written from a glance at the picture rather
than from the data, so run the number even when you have just looked at the plot that
contains it. Second, a question's prose is inside a numbered list, so a line of prose
that *begins* with a number and a period becomes a new list item and silently restarts
the numbering. A sentence that wrapped to "942. That imbalance is a fact about..." was
rendering as question 942. Rewrap the line.

The claims most likely to be invented are the ones about *what the data is*, because they
are the ones no code checks. Notebook12 first said the zero-calorie items were "water,
black coffee, diet soda, sugarless gum" and notebook13 first said the condiment hump was
missing from lunches eaten out. Both were written from plausibility. Joined against
`wweia_meta.csv`, the zeros are 92 percent water (11,069 bottled and 10,111 from the tap,
with decaf coffee a distant third at 272), and the tiny-item share is actually *higher*
away from home than at it. Both sentences are now the true ones. You may use tables the
students cannot join yet to check yourself; you just cannot ask them to.

Notebook14 hit the same trap twice, and it is worth seeing how it hides in a sentence that
is doing rhetorical work. The draft said a cast list can name the Witches once but a script
"has to know which one says 'Double, double toil and trouble'", which is a good line and is
false: the data assigns that refrain to all three Witches at once, in the very multi-speaker
cell the question is about. The draft also said the worst packed cell held four names. It
holds ten. Both errors were confident, both were decorative, and neither would have raised
an error. **Check the example, not just the number.** A quotation chosen to illustrate a
point is a claim about the data like any other.

Notebook19 hit it a third time, in the same position, which is enough of a pattern to name.
Having found that Allegiant is the only airline at St Petersburg and Orlando Sanford, the
draft reached for a contrast and wrote that "Sarasota is the same idea and Allegiant does not
go there either; Southwest and Delta do." Allegiant flies to Sarasota. It is one of only four
places Allegiant goes from Richmond, and the *real* pattern is cleaner than the invented one:
Allegiant serves all three secondary airports and neither of the primary ones. So the rule is
sharper than "check the example." **The sentence most likely to be false is the one completing
a rhetorical turn.** A number gets checked because it looks like a claim. A contrast, a
counterexample, or an "of course, X is different" gets written because the paragraph wanted it,
and it slides past unverified precisely because it is doing literary rather than evidentiary
work. Run those sentences first, and be suspicious of any clause that arrives to make a point
land.

Two mechanical notes from the same notebook, both about `.join_asof()`:

- The default `coalesce=True` **drops the matched row's key from the output**, which is the one
  column you need to find out whether the match was any good. An asof join answers every row by
  construction, so `coalesce=False` and a computed gap is not an optional flourish; it is the
  only check available. Any asof question should include it.
- Sorting the gap column with `descending=True` to find the worst match puts the *nulls* on top,
  since Polars sorts nulls first on a descending sort, and the rows with no match at all have a
  null gap. The first draft of the "worst staleness" block printed three rows of nulls. It needs
  a `.drop_nulls()` before the sort. This is notebook09's lesson arriving as a bug three notebooks
  later, which is the argument for the tool ledger.

Notebook20 adds a rule about *absence*, which is the one kind of error none of the checks above can
catch. Every verification trick in this section confirms a claim about rows that are in the table. The
Shakespeare corpus is missing a fifth of itself, no `null` marks the gap, `null_count()` is zero, every
key is unique, every join matches, and the tables are internally consistent to the last row. The only
thing that gives it away is a column that *counts*: the line numbers run to 101,886 and the table has
80,592 rows. So when a table has an ordinal or an identifier with a natural sequence in it, check that
the sequence has no holes, because a filter run upstream leaves no other fingerprint. And treat a column
with a single distinct value as a suspect rather than a nuisance: it is often the name of the filter.

The corollary is a warning about writing prose from the data you can see. Notebook14 said the corpus
labels the gravediggers and Falstaff as `verse`, "including every scene of prose the man ever wrote."
It was checkable and it was wrong, and it was wrong in the direction of assuming that what is in the
table is what exists. Falstaff has eight lines in *1 Henry IV*, and the sentence would have been caught
by a single `.filter()` that nobody thought to run because nobody thought there was anything to find.

Two mechanical notes from the same notebook, both about making a student *see* a row:

- `.print(n)` from `funs.py` sets `tbl_rows=n`, and Polars renders a longer frame as a head
  and a tail with the middle elided. So `.print(20)` on a 49-row frame does not show twenty
  rows; it shows nine, an ellipsis, and eight. If a question turns on a row the student has
  to notice, slice the frame with `.head(n)` first and print that. The multi-speaker cell in
  notebook14's Macbeth question sat in the elided middle for a whole draft.
- A `.sort()` does not break ties in a stable way across runs. The same cell tied at 21 lines
  with two other speakers and moved between ranks 17 and 19 from one execution to the next. A
  `.head(n)` that must contain a particular row needs slack, so leave a few rows of margin
  and do not write prose that names its exact position.

