# Building the Practice Notebooks (DSST289)

Working notes for writing and revising the `notebookNN.qmd` files in this
directory. Each notebook is a set of in-class practice questions with the
answers filled in; `qmd_to_ipynb.py` at the repo root turns them into the
student (`nb/`) and solutions (`nb_full/`) `.ipynb` files.

The longer guide that used to live here was deleted in commit `4d3e1923`
(2026-07-21); `git show 4d3e1923^:nb289/NOTEBOOKS.md` recovers it. The DSST389
counterpart, `nb389/NOTEBOOKS.md`, is still current and follows the same house
style.

## Simplification rules (October 2026)

These rules come from the instructor after early drafts proved too hard for
the class. They were written for the DSST389 notebooks and apply here too.
Where anything in the old guide disagrees with them, these rules win.

1. **Never save an intermediate dataset in a student answer.** Students who
   save a table and later change it end up with different versions of the
   data. Have them repeat the chain instead ("Take the code from the previous
   question and ..."). If a saved table is truly needed, write the code
   yourself in a `#| tags: [noclear]` block so every student has the same
   version. Never overwrite an existing dataset; save the result under a new
   name so the block gives the same result when run twice. A block that is
   safe to re-run this way can be left for students to write.
2. **One code block per question.** If an answer needs two blocks, make it
   two questions.
3. **No questions that only check that something works.** Key checks, row
   counts compared against an expected number, reconstruct-and-compare,
   "confirm that ...", and summary statistics that restate a plot all
   confused students. Keep a question only if it produces a finding of its
   own.
4. **Start easy and keep the end short.** Open with a few very simple
   warm-up questions on earlier material (filter, sort, `group_by`/`agg`, a
   plotnine plot) before the chapter's new tools. Cut the most complicated
   late questions instead of keeping them; ending on a simple question is
   fine.

## In practice

- Aim for roughly ten to twenty short questions, each asking for one thing.
  A longer task becomes a sequence of questions that each repeat the
  previous chain and add one step.
- Include plots throughout (`geom_point`, `geom_line`, `geom_col`), not only
  tables.
- Practice what the chapter taught before trying anything clever. Avoid
  questions built around pitfalls (NaN/inf, null sorting) unless the chapter
  teaches that pitfall.
- When a needed step uses code the chapter has not taught yet, give it as a
  `noclear` block instead of asking students to write it.
- Keep commentary after a code block to one to three plain sentences, and
  check every number in it by running the notebook. Make sure the rows the
  commentary talks about are visible in the printed output, since Polars
  hides middle rows.
- After editing, renumber the questions, fix every "question N" reference,
  run every block, and regenerate the notebooks with
  `.venv/bin/python qmd_to_ipynb.py` from the repo root.

The revised `nb289/notebook11.qmd` and `nb389/notebook39.qmd`–`notebook40.qmd`
are good models.
