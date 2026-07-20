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
| 48 | 17.7–17.9 | reading a precomputed dense embedding column (`vit`, `siglip`) as a Polars `List` and checking it is 768-long and genuinely dense — `explode`ing the list so every scalar becomes a row and finding *zero* exact zeros in 768,000 values, the concrete contrast with notebook42's ~97%-zero TF-IDF matrix that turns the chapter's "dense, not sparse" prose into a number; `ViTEmbedder()` loading a pretrained network and `c.filepath.map_elements(vit, ...)` embedding an image live, with transfer learning made concrete by re-embedding three images and confirming `dot_product(c.vit, c.vit_live)` ≈ 1.0 against the stored column (the "don't trust a precomputed column blindly" spot-check, done on three rows because the full 1,000 is slow — which is *why* the column ships precomputed); `umap(features=[c.vit], n_components=2, random_state=42).predict(full=True)` projecting the 768-dim embeddings and a `geom_point(aes(color=c.label))` scatter that separates the ten breeds well but *not* cleanly (Samoyed/sheepdog islands, hounds and terriers bleeding together), the honest fine-grained contrast with the chapter's near-perfect bird *species* separation; the notebook42 2D same-label nearest-neighbor rate reused on image coordinates (0.93 overall against a 10% chance rate, English foxhound lowest at 0.81 and also the smallest class at 62 images, Samoyed/sheepdog ~0.98), measuring the projection instead of eyeballing it; `SigLIPEmbedder()` and `embed_text` embedding a natural-language prompt into the *same* space as the image column, a single `"a photo of a golden retriever"` prompt scored by `dot_product(c.siglip, c.siglip_txt)` over a `join(embed, how="cross")` and spot-checked by plotting the top-8 images (all golden retrievers) rather than trusting the score; full zero-shot classification by embedding all ten cleaned breed names (`pl.lit("a photo of a ") + c.text.str.replace_all("_", " ")`), `group_by(c.filepath).head(1)` to take each image's best label, and `(c.label == c.text).mean()` for a 0.92 class rate on ten fine-grained breeds with no training; a deliberate wrong-space failure that swaps `c.siglip` for `c.vit` in the dot product and collapses the rate to 0.13 (barely above chance) with similarity scores in a narrow band around zero — no error raised, every image still gets a tidy prediction, catchable only by knowing ViT image vectors and SigLIP text vectors were never trained to share a space; the chapter's own misclassification grid (`label => predicted`) reused on breeds, with errors falling into two verifiable-by-eye kinds — genuinely look-alike breeds (beagle↔foxhound, terrier→small shaggy dog) and cropped/turned-away/multi-subject frames where the breed's features are not visible; a per-breed zero-shot accuracy (beagle 0.79, foxhound 0.82, aussie terrier 0.85 hardest; sheepdog/Samoyed near-perfect) shown to reproduce the *same* hard-breed ordering the unsupervised UMAP NN rate gave, two unrelated methods (one on ViT, one on SigLIP) agreeing that the difficulty is in the breeds, not the method; a `group_by(c.index)` check that the benchmark's train/test split is irrelevant to a zero-shot classifier (rates near-equal, `test` if anything *higher*, because nothing was fit and so nothing can overfit), the split reframed as a supervised-era leftover; and a closing written question on why an unsupervised projection and a text-driven classifier fail on the same categories — because both read the image only through an embedding of visual appearance, so two breeds that look alike to a person look alike to every method built on the vectors, the flip side of the chapter's embedding optimism |
| 47 | 17.1–17.6 | `cv2.imread` returning an image as a NumPy `height × width × 3` array of 0–255 bytes, `.shape` and `.mean()` on it; that OpenCV stores channels in BGR order, made concrete by per-channel means on a warm frame where channel 0 (blue, 56.1) is *lower* than channel 2 (red, 63.8), so a student assuming channel 0 is red misreads the frame; that a real-world collection is not resized to a common grid the way a benchmark set is (500 FSA-OWI images span 105 distinct `(height, width)` sizes, 394 landscape to 106 portrait, all 640 on the long side), caught by looping `cv2.imread` to build a `pl.struct("height","width").n_unique()` check and pushing the lesson that any per-image statistic must be size-independent (a `.mean()` works, a fixed-pixel index would not); looping `cv2.imread` over `fsac.iter_rows` to append a `brightness` column via `pl.Series`; `DSImage.plot_image_grid(..., label_name=)` to eyeball a sorted head, with the darkest twelve landing on Jack Delano's around-the-clock Chicago rail-yard night shots and Alfred Palmer's inside-a-tank frame, the chapter's "brightness is the background, not the subject" limitation shown rather than asserted; a `brightness` boxplot restricted to photographers with `pl.len().over(c.photographer) >= 20` and ordered by `c.brightness.mean().over(...)`, revealing that the two darkest photographers (Palmer, Hollem, both ~60) are exactly the ones assigned to artificially-lit aircraft and defense plants while the outdoor shooters (Collier, Delano, ~80–87) are brightest — a `.geom_boxplot().coord_flip()` on assignment, not merit; `cv2.cvtColor(img, cv2.COLOR_BGR2HSV)` leaving shape unchanged and packing hue into [0,179]; `DSImage.compute_colors` returning per-hue-bucket *percentages* plus a `neutral` bucket that sum to 100, and catching that the chapter's own prose ("proportions sum to 1") disagrees with its helper's actual output, checkable only by adding the numbers; the corpus's warm cast quantified (`neutral` ~68%, `orange` ~16% the dominant hue — skin, wood, brick, dirt — against `blue` ~8% and `red` <3%) via `pl.concat([fsac, results], how="horizontal")` then `.mean()`; a BGR deliberate failure where the reddest image run through `cv2.COLOR_RGB2HSV` (wrong) instead of `COLOR_BGR2HSV` swaps red and blue (33%/5% → 5%/49%) with no error and a tidy dict that still sums to 100, so only knowing the image is red flags it; that a color proportion, like brightness, finds red *things* (schoolchildren's clothing, a Court-day courthouse square, a scrap-and-salvage depot, a tractor) rather than any single subject; and a closing `group_by(photographer)` pipeline over brightness/orange/blue that reads as real, stable per-photographer differences (Wolcott most orange and almost never blue; Palmer/Hollem more blue, less orange) while making the chapter's central point that pixel features separate a wheat field from a factory floor by light and color but can never tell two differently-lit frames of the same subject apart, the gap the embeddings in 17.7–17.9 exist to close |
| 46 | 16.6–16.10 | building a co-citation edge list from a raw citation table by self-joining `cite` to itself on `citing_case` (the join-chapter self-join reused to turn "who cites whom" into "who is cited alongside whom"), keeping each unordered pair once with `c.cited_case < c.cited_case_right` and counting shared citers; that a co-citation network of the same 80 cases fragments into three components under a `count >= 15` threshold where the direct-citation network was one connected piece (a 68-case rights core plus two two-case islands, *Furman*/*Gregg* death penalty and *Standard Oil*/*Socony* antitrust, that are heavily co-cited with each other but share no third citer with the core), the component-count discipline from notebook45 recurring; that co-citation eigenvalue centrality crowns an entirely different neighborhood (*Cantwell*, *Schneider*, *Whitney*, *NYT v. Sullivan* — the First Amendment cases) than direct-citation degree did (*Palko* and criminal procedure), because co-citation rewards being cited *in company* rather than being cited *often*, and the SCOTUS record shows the citation/co-citation gap the chapter says Wikipedia is too edit-scrambled to show; `DSNetwork.process(directed=True)` returning `degree_out`/`degree_in`/`degree_total` and dropping closeness, with the directed in-degree-vs-out-degree scatter (chapter's own plot) revealing a temporal structure a court has and Wikipedia does not — oldest cases (`McCulloch` 1819, out-degree 0) top-left, newest (`Buckley` 1976, in-degree 0) bottom-right — quantified as `pl.corr(term, degree_out)` = 0.63 against `pl.corr(term, degree_in)` = −0.25 and a count of the 10 cases citing none of the other 79, the "there is no temporal ordering" caveat the chapter raises for Wikipedia turned into a checkable clock; building a distance between cases with no text at all by treating each case's set of incoming citers as an indicator vector and computing the angle distance by hand (`.pivot().fill_null(0).to_numpy()`, normalize, `arccos(X @ X.T)` — notebook42's from-scratch distance pattern) so two cases are close when their citing audiences overlap, spot-checked against known doctrine (*Furman*/*Gregg* nearest at 0.85, *Meyer*/*Pierce* substantive due process next); the π/2 orthogonality problem from notebook42 recurring on citation profiles (mean distance 1.53 of a 1.5708 max, 829 of 3,160 pairs sharing zero citers) so a fixed distance cutoff either shatters the network (11 components at 1.4) or over-connects it (near-complete at 1.5), motivating ranks over thresholds; the symmetric nearest-neighbor network built in Polars by stacking the pair table with a column-swapped copy, taking each case's `k=5` nearest with `group_by(maintain_order=True).head(k)`, and keeping only mutual pairs via a `min_horizontal`/`max_horizontal` canonicalization filtered to `mutual == 2`, giving a single 77-node component with max degree exactly `k`; the chapter's central claim that eigenvalue and betweenness decouple in a symmetric-NN network made concrete (`pl.corr(eigen, between)` = −0.14 against the direct network's +0.37) with *Brown v. Board* as the highest-betweenness node at near-zero eigenvalue, the gatekeeper the other networks buried among the hubs; walktrap communities on the balanced network recovering recognizable doctrine (Fourth Amendment: *Weeks*/*Carroll*/*Olmstead*/*Katz*/*Mapp*; incorporation: *Hurtado*/*Palko*/*Malloy*/*Duncan*) more evenly than the direct network's; and a closing written question asking which of the four networks (direct-citation, co-citation, directed, nearest-neighbor) answers "most influential precedent" / "which doctrines are treated as related" / "which case bridges separate lines of law", the chapter's real point that the network you build decides what you can see |
| 45 | 16.1–16.5 | `DSNetwork.process(edge_list, directed=False)` returning the `(node, edge, G)` triple, the node table's centrality columns (`component`/`component_size`/`degree`/`eigen`/`close`/`between`/`cluster`) and the edge table's `x`/`y`/`xend`/`yend` for a `geom_segment` layer; building an induced-subgraph edge list by filtering a raw citation table (`scotus_citation`) to the edges whose two endpoints both fall in a chosen node set and renaming `citing_case`/`cited_case` to `doc_id`/`doc_id2`; a deterministic second sort key (`.sort([c.n_in, c.cited_case], descending=[True, False])`) so a top-80 cut with ties at the boundary reproduces identically run to run, the "numbers that rot" fix applied at selection time rather than caught afterward; the node-count discipline that 80 selected cases yield only 77 network nodes because an edge list silently omits any node in no edge, caught with an anti-join and landing on three heavily-cited but topically-unrelated dropouts (*Chevron*, *Pennoyer v. Neff*, *Mathews v. Eldridge*, all administrative/civil-procedure cases with no citation tie to the constitutional-rights core) rather than an error; raw in-degree (`group_by(c.cited_case).agg(pl.len())`) crowning *McCulloch* as most-cited corpus-wide while network `degree` within the induced set crowns *Palko v. Connecticut* instead, since degree here counts only ties among the 80 landmarks and *Palko* is cited by many of those later rights cases while *McCulloch*'s 255 citations come mostly from ordinary cases outside the set; the four centrality measures colored on a Fruchterman-Reingold layout, with betweenness genuinely separating from eigenvalue on this multi-domain network (*Ashwander* and *McCulloch* scoring near the top on betweenness at degree 8 and eigenvalue ~0.1, as bridges between the federalism cluster and the rights clusters) where the chapter's own single-cluster author network explicitly could not show the difference; `community_walktrap` clusters mapping onto recognizable areas of law, verified by reading members rather than asserted (a clean seven-case Fourth Amendment cluster: *Boyd*, *Weeks*, *Carroll*, *Olmstead*, *Katz*, *Terry*, *Bivens*, plus a two-node antitrust island of *Standard Oil* and *Socony*); a phantom node (`75 U.S. 168`, cited enough to reach the top 80 but absent from the `scotus_case` metadata, so `case_name` is null after a left join) tied to 3,705 distinct cited cases the metadata table never covers, the annotation/embedding spot-check-against-known discipline applied to network nodes; `case_name` failing an `n_unique`-versus-`len` key check (863 rows share a name with another case) so every edge and node is keyed on the reporter `citation` and never the name, the not-a-key lesson in a legal-citation guise; and closing by measuring the eigen/between relationship the chapter only gestures at with `pl.corr` (0.91 for degree-versus-eigenvalue against 0.37 for eigenvalue-versus-betweenness), the bridge cases alone pulling the second pair far below the first, a checkable number in place of eyeballing two nearly identical colored plots |
| 43 | 15.6–15.7 | anti-joining a bilingual text table against itself to find which authors lack a translation at all, then ranking the full corpus by page length to show the two missing French pages belong to the corpus's shortest and third-shortest English ones — translation coverage tracking obscurity, discovered rather than asserted; running the chapter's own `DSText.process`/`compute_tfidf`/`compute_distances`/`umap_text` pipeline completely unmodified against `fr_core_news_sm` in place of `en_core_web_sm`, since none of the wrapper code has any language-specific logic in it; catching a real gap between the chapter's own prose and its own rendered output — the `max_df=1.0` top-terms call the "Across Languages" section actually uses produces stopword-dominated lists (`the`/`of`/`and` in English, `de`/`le`/`à` in French) in both languages, confirmed against the book's own rendered table for the full 75-author English corpus, and only the stricter `max_df=0.5` used elsewhere in the same chapter delivers the clean, name-dominated lists the prose describes; a leaked-CSS scraping artifact (`mw-parser-output`, from a hidden Wikipedia geo-coordinate template) found via `str.count_matches()` in exactly 4 of 73 English pages and zero French ones, tagged as an ordinary alphabetic `NOUN` by spaCy so `is_alpha` does not catch it the way notebook41's backslash artifact was caught; reproducing the chapter's English/French part-of-speech proportion comparison on the exact matched 73-author subset both tables share, unlike the chapter's own version which silently stacks 75 English pages against 73 French ones; a cross-lingual nearest-neighbor agreement rate (47.9%, 35 of 73 authors) computed by finding each author's angle-distance nearest neighbor separately in each language and checking how often the two languages agree, as a checkable stand-in for the chapter's own hand-wavy "if the projections differ..." framing; testing and rejecting a plausible-looking causal story by recomputing a distance with a suspect term (`parser`) removed and finding the result barely moves (1.528 to 1.548) and the nearest neighbor does not change, a caution against attributing a nearest-neighbor result to whatever term happens to be visible in a short printed list; and a same-era nearest-neighbor rate computed directly on both UMAP projections' `dr0`/`dr1` coordinates (20.5% English, 26.0% French, against a roughly 17% chance rate for seven uneven era categories) as a quantitative check on "loose" era clustering, continuing notebook42's practice of measuring a projection instead of just eyeballing it |
| 42 | 15.4–15.5 | pivoting a long TF-IDF table into a two-term scatter (`olympic`/`profit`) that lands on a cleaner separation than the book's own `poem`/`novel` example — zero documents nonzero on both axes here, since AG News's topics are disjoint by construction where the book's authors genuinely mix poetry and prose; a matrix-sparsity check (`.pivot().fill_null(0).to_numpy()`, then a plain `(X == 0).sum()`) that turns the chapter's "sparse embedding" description into a number, 97.4% zero cells and about 24 nonzero terms per document out of a 917-word vocabulary; `umap_text(..., random_state=)` for a reproducible 2D projection, paired with a same-label nearest-neighbor rate computed directly on the projected `dr0`/`dr1` coordinates (50% overall, twice chance for four labels but far short of the book's clean author clusters) as a checkable stand-in for eyeballing a plot; `DSText.compute_distances()` with its row count verified against $\binom{200}{2}$; stacking a one-row-per-pair distance table with a column-swapped copy of itself via `pl.concat` to get both directions; the `group_by(doc_id).head(1)` nearest-neighbor pattern applied to the full-dimensional angle distances (70% same-label overall) and shown to rank the four topics in the same order (`Sports` easiest, `Sci/Tech` hardest) as the cruder 2D version; a from-scratch raw Euclidean distance built with the same `to_numpy()` pivot the chapter's own reference code uses for the angle distance, reproducing the chapter's length-distortion warning concretely: two long articles (95 and 137 tokens against a 39-token average) get picked as the Euclidean nearest neighbor for 136 of 200 documents (68%) regardless of topic, while the angle distance on the same corpus correctly matches a `World` article about a Vancouver police case to a different `World` article about a Vancouver police case instead of a `Sci/Tech` virus story; spot-checking the single globally closest pair by reading both articles' full text, landing on a genuine AG News near-duplicate (two independently filed Reuters stories, minutes apart, about the same Medtronic earnings release); and the $\pi/2$ maximum-distance case explained by IDF, where a spaCy tokenizer splitting one rare Dutch surname into three separate tokens is enough to make a 16-term document share no filtered vocabulary with 162 of the other 199 |
| 40 | 14.5–14.10 | `.shift(-1).over([c.doc_id, c.sid])` on `lemma`/`is_alpha` pairs to build a bigram table without a sentence boundary leaking across rows, and the same shift extended to `-2` for trigrams; PMI computed by joining per-word counts onto per-bigram counts and comparing `p_bigram` to `p_w1 * p_w2` on a log scale, with the `bigram_count >= 5` floor that keeps rare-word noise out of the ranking; that a high-PMI list is not simply "rare proper nouns," since this corpus's top-15 mixes proper nouns with review-voice phrasing ("my opinion", "apart from") and genre vocabulary ("sci fi", "production value") that a biography corpus never produces; the `ent_iob == "B"` cumulative-sum trick (`.cum_sum().over(c.doc_id)`) that turns per-token entity labels into per-entity groups, reused on a corpus where a `PERSON` label means a real director (Josh Kornbluth) as often as a fictional character (John Baird), distinguishable only by reading the surrounding text, not the label; a `dep`/`head_idx` join (the same "share a head" pattern behind the chapter's own subject-verb pairs) used to find negated predicate adjectives (`dep in ["acomp", "attr"]` sharing a head with a `dep == "neg"` token) regardless of how many words separate the negation from what it negates, catching 76 instances where a `shift(-1)` bigram search modeled on question 1 would have caught only the 30 where the negation sits directly next to the adjective; restricting an `amod` adjective-noun join to a specific head noun (`movie`/`film`) to sharpen a sentiment signal notebook39 found only partially in raw counts — it works for `bad` (16 negative "bad movie"/"bad film" uses against 1 positive, versus 86-to-17 for the bare word anywhere in a review) but not for `good`, which stays almost as evenly split as notebook39's own raw count; `DSText.kwic()` run on a corpus where a single keyword's surrounding context ranges across the full sentiment scale within ten printed lines, unlike the more uniform register of a biography page; four complexity metrics (mean sentence length, type-token ratio, mean word length, content-word ratio) computed per document and shown to barely separate `positive` from `negative` reviews, against a plain count of `"!"` tokens, which does (1.21 per negative review versus 0.52 per positive one) — evidence that a genre's sentiment can hide from every metric the chapter introduces and still turn up in a `.filter()` on a single punctuation mark |
| 38 | 13.7–13.12 | casting elapsed milliseconds to `pl.Datetime("ms")` via `.cast(pl.Int64).cast(pl.Datetime("ms"))`, the same trick a Unix timestamp already relies on, to get a real `Datetime` (and `.dt.truncate()`) out of a column with no calendar behind it, anchored at an arbitrary but shared reference so every session's elapsed time lands on the same clock; `.dt.truncate()` used to bucket one session's keystrokes into 10-second bins, and then, because the anchor is shared across all 823 sessions, to pool everyone's Nth minute together and read a corpus-wide trend (hold time rising 73.7 → 81.7 ms over 15 minutes) off a single `group_by()`; treating an already-supplied column (`dur_after`) as a claim to verify rather than a fact, checked against `c.dur.shift(-1).over(c.id)` before it is trusted; `.shift(1).over(c.id)` reaching across two different columns (`press` minus the previous row's `release`) rather than one, to build a `gap` duration `.diff()` cannot express; a duration column's fragility at the individual level (one 43-minute gap pushing a person to the third-highest average of 823) against its stability in bulk (dropping that person's rows moves the corpus average by 2 ms out of 457.7); `.rolling_mean_by(by=, window_size=)` to smooth an unevenly-spaced series by a span of time; the concrete cost of skipping `.over()` on a pooled rolling window, worse than the chapter's own warning suggests here specifically because the anchor trick makes hundreds of unrelated sessions (393, in one 15-second slice) share the same clock reading, so the ungrouped average is not just wrong but meaningless; `.join_asof(by=, strategy="backward")` matching every keystroke back to the most recent long pause to test a "restart cost" hypothesis, alongside the caution that the result is confounded with an already-known time-in-session trend; `.join_where()` as a self-join on an interval-overlap condition (`press_right < release & release_right > press`) to test for keyboard rollover, returning zero matches, confirmed cheaply at corpus scale with a plain `.min()` on the `gap` column instead of repeating the self-join everywhere |
| 39 | 14.1–14.4 | `spacy.load("en_core_web_sm")` and the callout warning that the model has to be downloaded once (`python -m spacy download en_core_web_sm`) before it can be loaded; `DSText.process(docs, nlp)` as three nested loops (documents, sentences, tokens) flattened into one token-per-row table, and reading its reference implementation before running it at scale; the `anno` table's columns (`token`, `token_with_ws`, `lemma`, `upos`, `tag`, `is_alpha`/`is_stop`/`is_punct`, plus `dep`/`head_idx`/`ent_type`/`ent_iob` reserved for later sections) and `(doc_id, sid, tid)` as its compound key, checked with the same `.group_by().agg().filter()` idiom chapters 8/9 used for any other table's key; reconstructing a document's original text by sorting on `sid`/`tid` and joining `token_with_ws`, confirming the annotation table is a lossless re-encoding of the input; that `upos == "NOUN"`/`"ADJ"` filtering has no `is_alpha` check built in, so unclean input tokens (an HTML `<br />` fused onto an adjacent word) can be tagged `NOUN` and inflate a frequency count with no error raised, demonstrated first on one document and then measured at corpus scale (`movie` and `film` undercounted by 8 and 6 out of roughly 440 and 346) once the same contamination runs through all 200 reviews uncleaned; grouping token counts by an external label column (joined in from outside `anno`) rather than by `doc_id`, as the general shape of "which words characterize which subset of documents"; that a raw word count can fail to separate two classes even when the words are intuitively diagnostic, because negation (`"not good"`) leaves the positive word in place while flipping the sentence's sense, tying back to the chapter's own "not bad" example from its introduction |
| 37 | 13.1–13.6 | that a bare row number lies about spacing and can splice unrelated events into a false single sequence, since Atlantic storm names recycle on a six-year rotation and `name` alone is not a key (the join-chapter lesson recurring in a temporal disguise); the fractional-year formula extended with an hour term; `pl.date(c.year, c.month, c.day)` built from separately-stored components, giving sensible plotnine axis labeling for free; `scale_x_date(date_breaks=, date_labels=)` with `element_text(angle=, hjust=)` to keep dense labels readable; `.dt.weekday()` used as a negative check (a flat result across weekdays confirms a physical process with no reason to follow the human calendar, unlike page views); filtering with a constructed `pl.date()`/`pl.datetime()` value; `pl.datetime(c.year, c.month, c.day, c.hour)` for a precision finer than a day, and that switching from `date` to `moment` removes a same-day staircase in a line plot; the strict `>` boundary excluding a row at the exact comparison timestamp; `.dt.replace_time_zone("UTC")` to attach a zone to a naive datetime versus `.dt.convert_time_zone()` to recompute the clock reading in another zone, and the concrete, checkable five-hour gap that appears when the two are swapped (replacing the zone label on an already-aware column instead of converting it) |
| 35 | 12.1–12.9 | sending an HTTP GET with `session.get(url, params=, headers=)` and reading `response.status_code`; parsing `.json()` and hand-flattening a nested response (`data["query"]["pages"]`, keyed by numeric page ID) into row dictionaries for `pl.DataFrame`; `requests_cache.CachedSession` with `allowable_codes=(200, 404)` and `expire_after=None` as a pipeline's raw layer, and `response.from_cache` to confirm a repeated call never left the machine; the `polite_get()` pattern (clearing `session.cookies` before every call, since Wikimedia's `Vary: Cookie` header would otherwise defeat the cache; `.raise_for_status()`; a 0.2s sleep skipped on cache hits) as the minimum politeness contract for a free API; defining a population from `list=categorymembers`, `cmtype="page"` to exclude subcategories, and `continue`-block pagination; deduplicating a category-derived spine with `.unique(subset="page_id", keep="first")`; the two-identifier pattern (`page_id` stable, `doc_id` readable) carried into every later table with a join; `redirects=1` and reading the `redirects` block versus a `pages[...].missing` flag; that a plain title landing on a real, unflagged page is not proof it is the *right* page: a name shared with someone else on Wikipedia resolves cleanly to a disambiguation page, with no error and no `missing` flag, silently substituting the wrong subject; `prop=extracts` with `explaintext=1` for one page of plain-text article body per request; spot-checking collected text against a known fact and against a keyword search (`.str.contains()`), and cross-checking one collected number (`.str.len_chars()`) against an independently-requested one (`prop=info`'s `length`) with `pl.corr()` |
| 31 | 11.1–11.5 | the `geo` namespace registered by `import funs`, reachable as `.geo.<method>` on any Polars DataFrame; the `geometry` column as WKT text and the `_crs` helper column; building WKT by hand with `pl.format("POINT ({} {})", c.lon, c.lat)`, and that `POINT` is written longitude first, so swapping the order builds a valid but wrong geometry with no error; `.geo.points_from_xy(x, y)` as the safe way to build points and record a CRS (default EPSG:4326); coordinate reference systems and EPSG codes; `.geo.to_crs()` to reproject; `geom_map()` with `coord_fixed()` for a to-scale static map, against a plain `geom_point()` scatter, which has no CRS and no scale; `.geo.explore()` for an interactive Folium map, with `tooltip=` taking plain column name strings rather than `c.` expressions; chaining `.filter()` straight into `.geo.explore()` |
| 32 | 11.6–11.8 | reading polygons from a GeoJSON file with `funs.read_file()` (returns a `geometry` column of `MULTIPOLYGON` WKT, loaded in EPSG:4326); that polygons need `geom_map()`, not `geom_point()` (there is no single x/y), and `geom_map(fill=, color=)` for outline/fill; `.geo.area`, which silently returns nonsense squared-degrees on an unprojected table and real square meters only after `.geo.to_crs()`; `.geo.centroid` as a *property* (no parentheses) that swaps each polygon for its center `POINT`, may land outside a concave/multi-part shape, and does not overwrite the table unless assigned back; choropleths as a `fill=` aesthetic on `geom_map()`, and the absolute-count-vs-area-based-rate caution (large provinces dominate the eye, so encode a density, not a raw total); the `.n_unique() == len()` key check applied to a polygon table before joining an aggregated attribute table (`covid` totals) onto it |
| 33 | 11.9–11.10 | `.geo.sjoin()` for a point-in-polygon spatial join, matching each point to the polygon that contains it with no shared key column; that both tables must be projected to the *same* CRS first (a mismatch does not raise a clean error, it surfaces as a confusing `ArrowTypeError`, so project both up front); that a spatial join is an inner join by default and silently drops any feature matching nothing, making row-count-before-vs-after the geometry analogue of notebook32's `.n_unique() == len()` key check; the `_left`/`_right` suffixes and the `index_right` bookkeeping column; that the *left* table's geometry is the one kept, so reversing operand order (`prov.geo.sjoin(it_city)`) swaps which geometry survives and produces a one-to-many result (polygon duplicated per contained point); grouping a join result to answer a question neither table holds alone (cities-per-province, urban population per province); `predicate=` (touches/intersects/contains/within/crosses/overlaps) with a `touches` self-join to recover shared borders, and that each undirected border appears twice; `.geo.sjoin_nearest(other, exclusive=True, distance_col=)` for proximity matching, distances in CRS units (meters when projected), and that running it unprojected returns degree distances that quietly *reorder* the ranking (a checkable flip, the notebook32 area-in-degrees trap in a new guise) |
| 34 | 11.11–11.15 | `.geo.buffer(distance)` to expand a point or polygon outward by a fixed distance in CRS units, turning points into discs; that buffering before an `.geo.sjoin()` changes an inner-join containment question into a proximity question, so row counts jumping upward (388 to 1,110 here) means overlap, not error; `.geo.dissolve(by=, aggfunc=)` as the spatial counterpart of `group_by`/`agg`, merging every polygon sharing a key into one and erasing the internal boundaries, with the group key returned as a plain column; `.geo.explode()` as dissolve's inverse, splitting every multi-part geometry into one row per part and copying the whole-feature columns onto each part unchanged, so a metric like `.geo.area` needs recomputing after an explode to mean anything at the part level; that a high post-explode part count does not by itself mean real islands, since a boundary file can carry dozens of sub-hectare digitization slivers for a province with no coastline features at all, only comparing the actual areas tells the two cases apart; `.geo.count_coordinates()` to total a table's vertices, and `.geo.simplify(tolerance)` to reduce them at a cost in boundary accuracy measured in CRS units, with the caveat that independent per-geometry simplification can open gaps between formerly shared borders; `.geo.is_valid` as a property to check for topologically broken polygons before trusting anything computed from them, tying together the chapter's Best Practices list (CRS mismatches, unprojected calculations, invalid polygons, boundary effects) with concrete checks run earlier in the same notebook |

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
| 32 | Italian provinces + provincial COVID series | `data/it_province.geojson`, `data/it_province_covid.csv` |
| 33 | Italian cities + provinces together | `data/it_cities.csv`, `data/it_province.geojson` |
| 34 | All three Italy tables together | `data/it_cities.csv`, `data/it_province.geojson`, `data/it_province_covid.csv` |
| 35 | Turing Award laureates (collected live) | none — built from `Category:Turing Award laureates` via the MediaWiki Action API |
| 37 | North Atlantic tropical cyclone tracks | `data/storms.csv`, `data/storm_codes.csv` |
| 38 | Keystroke log of 823 English-language writers | `data/keylog.csv.gz`, `data/keylog-meta.csv.gz` |
| 39 | IMDb movie reviews (200-review subsample) | `data/imdb5k_pca.parquet` |
| 40 | IMDb movie reviews (same 200-review subsample as notebook39) | `data/imdb5k_pca.parquet` |
| 41 | AG News articles (200-article subsample, 4 categories) | `data/agnews_pca.parquet` |
| 42 | AG News articles (same 200-article subsample as notebook41) | `data/agnews_pca.parquet` |
| 43 | Wikipedia authors, English and French, narrowed to the 73 with both | `data/wiki_uk_meta.csv.gz`, `data/wiki_uk_authors_text.csv`, `data/wiki_uk_authors_text_fr.csv` |
| 45 | U.S. Supreme Court precedent network, restricted to the 80 most-cited cases | `data/scotus_case.csv`, `data/scotus_citation.csv` |
| 46 | Same SCOTUS 80-case network as notebook45, recut four ways | `data/scotus_case.csv`, `data/scotus_citation.csv` |
| 47 | FSA-OWI color photographs (500-image Library of Congress sample) | `data/fsac.csv` (+ `media/fsac/*.jpg`) |
| 48 | Imagewoof (1,000-image ten-dog-breed ImageNet subset, precomputed ViT + SigLIP embeddings) | `data/imagewoof_1000.parquet` (+ `media/imagewoof_1000/*.png`) |

Notebook48 takes Imagewoof over Imagenette (the two ImageNet subsets the
catalogue flags for exactly this half of the chapter) because 17.7–17.9 is the
embeddings half — transfer learning, UMAP, and zero-shot classification — and
its whole lesson is that a dense pretrained vector carries real *visual* meaning,
which lands harder on a dataset where that meaning is genuinely tested. The
chapter's own bird *species* separate almost perfectly under both ViT and SigLIP,
and Imagenette's ten distinct objects (church, gas pump, garbage truck) would
only repeat that clean result. Imagewoof is the deliberately hard sibling: ten
fine-grained dog breeds, several of which look alike, so the embeddings separate
them well but not perfectly, and that gap is the notebook's spine. It shows up
three times over as a checkable number rather than an assertion — a 0.93
UMAP nearest-neighbor rate with the English foxhound down at 0.81, a 0.92
zero-shot rate, and a per-breed accuracy that bottoms out on the beagle (0.79)
and the two hounds. The dataset earns the notebook on grounds Imagenette could
not supply: its confusions are ones a student can reason about from the pictures
(a beagle and an English foxhound are near-identical tricolor hounds, the two
terriers are both small and scruffy), so the misclassification grid is verifiable
by eye, and the same short list of hard breeds falls out of two unrelated methods
— an unsupervised UMAP projection of the ViT vectors and a text-driven SigLIP
classifier — which is the notebook's real payoff: when both agree, the difficulty
is in the breeds, not the method. Two features come for free. Both embedding
columns (`vit`, `siglip`) are precomputed and unit-normalized, so `dot_product`
is cosine similarity with no extra work, and because `vit` and `siglip` are the
same shape but from different models, the notebook's deliberate failure writes
itself: scoring the SigLIP *text* embedding against the ViT *image* column runs
without error, returns a tidy prediction for every image, and collapses to 0.13
— catchable only by knowing the two columns do not live in the same space. The
one honest note is that the underscore-slug-vs-clean-prompt story is *not* a
strong lesson here (cleaning the labels moves the rate barely 1%), so the
notebook cleans the prompts quietly and spends its deliberate-failure budget on
the wrong-space swap instead. Imagewoof is unused anywhere else in either
course's ledger; notebook47's FSA-OWI carries the pixel-statistics half, and the
two halves of chapter 17 want fundamentally different material (raw image files
versus precomputed dense vectors), so splitting them across two datasets costs
the reader no comparison.

Notebook47 takes the FSA-OWI color photographs over the other vision
candidates because 17.1–17.6 is the pixel-statistics half of the chapter —
reading an image as a raw array, then summarizing it by brightness and by
hue — and that half wants genuine color photography where brightness and
color *are* the material, not a benchmark of pre-standardized tiles. The
collection is the less-famous Kodachrome color work from the Library of
Congress's FSA-OWI project, so a color analysis is meaningful on its face
(the corpus has a real, checkable warm cast: `neutral` ~68%, `orange` ~16%
the dominant hue against `blue` ~8% and `red` under 3%, exactly the palette
of skin, wood, brick, and dirt in Depression-and-wartime documentary
scenes). The dataset earns the notebook on grounds the chapter's own bird
set cannot supply. Its natural grouping variable is the *photographer*, and
that turns the chapter's own "brightness reflects photographic context, not
the subject" caution into a sharper, checkable result: the two darkest
photographers on average (Alfred Palmer and Howard Hollem, both ~60) are
precisely the ones the war effort assigned to artificially-lit aircraft
factories and defense plants, while the outdoor shooters (John Collier, Jack
Delano, ~80–87) are brightest — brightness tracking assignment, verifiable
by reading the captions rather than asserted. The `caption` column gives
every extreme a spot-check for free (the darkest frames are Delano's
around-the-clock Chicago rail yard and Palmer's inside-a-tank shot; the
reddest are children's clothing, a Court-day square, a salvage depot),
which is the annotation the bird labels never carried. Two further features
come at no authoring cost: the images are genuinely *not* resized (500 photos
in 105 distinct sizes) where the chapter's birds were standardized, giving a
concrete size-independence lesson, and the BGR-ordering trap the chapter only
warns about becomes a real deliberate failure here, because running the
reddest frame through `COLOR_RGB2HSV` instead of `COLOR_BGR2HSV` swaps red and
blue (33%/5% → 5%/49%) with no error raised. The one honest wrinkle is that
`fsac` has no `vit`/`siglip` embeddings, so it cannot carry notebook48's
transfer-learning and zero-shot sections (17.7–17.9); those go to Imagenette
or Imagewoof, whose precomputed embeddings are exactly what that half needs.
The two halves of chapter 17 want fundamentally different things — raw pixel
files versus dense vectors — so splitting the dataset costs the reader no
comparison, unlike the SCOTUS and AG News pairs that genuinely shared one
table. FSA-OWI was used once in nb289's notebook17, but for reading imperfect
files, not pixel statistics, so the lesson here does not repeat it.

Notebook46 stays on notebook45's exact 80-most-cited SCOTUS set, the same way
the chapter's own second half stays on its Wikipedia author corpus: 16.6–16.10
are four *other* networks (co-citation, directed, distance, nearest-neighbor)
over the one edge list, so a fresh dataset would only cost the reader the direct
comparison that is the whole point. The dataset earns the repeat on grounds the
chapter's own examples explicitly cannot supply. The book warns that its
Wikipedia network is too small and too edit-scrambled to bring out the
differences between these network types — "there is no clear temporal ordering
of the pages," and the citation/co-citation gap is "somewhat muted" — and each
of those warnings becomes a concrete SCOTUS result. Co-citation on the court
record fragments into a rights core plus a death-penalty and an antitrust
island and crowns a different centrality winner (the First Amendment cases)
than direct citation did, the "striking" difference the chapter says only
non-Wikipedia data shows. The directed network's in/out degree scatter reveals
a clean temporal clock (corr of term with out-degree 0.63, with in-degree
−0.25; ten oldest cases citing none of the others) precisely because a court
opinion, unlike a Wikipedia page, can only cite backward. And the
nearest-neighbor network is where the chapter's headline claim — that
eigenvalue and betweenness centrality decouple in symmetric-NN networks — lands
as a checkable −0.14 correlation against the direct network's +0.37, with
*Brown v. Board* surfacing as the top-betweenness gatekeeper at near-zero
eigenvalue. The one real obstacle is that SCOTUS has no text in the catalogue,
so the distance and nearest-neighbor sections (built on text angle distances in
the book) need a distance from somewhere: the notebook builds one from the
citation structure itself, the angle between cases' incoming-citer indicator
vectors, which both keeps everything in the citation domain and re-triggers
notebook42's π/2 orthogonality finding (829 of 3,160 pairs share no citer at
all), turning "why a fixed cutoff fails and ranks succeed" into the motivation
for the nearest-neighbor section rather than an aside. SCOTUS remains unused
anywhere else in either course's ledger.

Notebook45 takes the SCOTUS citation network over the other network candidate,
the English Wikipedia link graph, because chapter 16's opening sections are
about building a network object and then plotting every node and edge to see
degree, eigenvalue, closeness, and betweenness centrality laid out, and that
needs a network small enough to actually draw. enwiki's 10 million edges are
the wrong size for the foundational half of the chapter (they belong to
notebook46's later, table-driven sections if anywhere); SCOTUS is the
candidate the ledger already flagged as "small enough to look at directly."
The chapter's own dataset is the `wiki_uk_citations` 75-author graph, so this
also satisfies the avoid-the-chapter's-dataset rule while staying in the
citation-network family the chapter is built around. Rather than run
centrality on all 24,071 cases (which cannot be plotted any more than enwiki
can), the notebook builds an induced subgraph of the 80 most-cited cases and
the links among them, which comes back a single connected component of 77
nodes and 327 edges, almost exactly the 75-node scale the chapter uses for its
own drawable example. The dataset earns the notebook on grounds the 75-author
graph could not supply. Its most-cited cases are landmark decisions an American
undergraduate can reason about (*McCulloch*, *Miranda*, *Gibbons*, *Gideon*),
so a wrong centrality ranking is visible to a reader without checking a key,
and the corpus spans several genuinely distinct areas of law rather than one
subject, which is what finally separates betweenness from the other centrality
measures: *Ashwander* and *McCulloch* score near the top on betweenness with a
degree of 8 and an eigenvalue near 0.1, as bridges between the commerce and
rights clusters, exactly the contrast the chapter says its own dense
single-cluster network is too small to show. The walktrap communities land on
recognizable legal domains a reader can verify (a clean seven-case Fourth
Amendment cluster), and the raw edge list carries its own checkable failures
for free: three heavily-cited cases (*Chevron* among them) drop silently out of
the induced network because they share no citation with the constitutional-law
core, one node (`75 U.S. 168`) is cited into the top 80 yet has no metadata row
at all, and `case_name` fails a key check on 863 rows, all of which turn the
chapter's implicit "keep track of what your nodes are" caution into concrete,
recognizable checks. SCOTUS is unused anywhere in either course's ledger.

Notebook43 does not get to avoid the chapter's own dataset, because
`wiki_uk_authors_text_fr.csv` is the only French-paired text in the whole
catalogue and there is no second bilingual corpus to reach for instead —
exactly the constraint flagged above before any notebook in this range was
drafted. What the notebook can still do is take the narrowing seriously
rather than paper over it. `text_fr` turns out to have only 73 of the 75
authors' pages, and the two missing ones, Rex Warner and Edward Upward, are
independently the shortest and third-shortest English pages in the entire
corpus — a genuine, checkable finding (translation coverage tracks
obscurity, not era) that becomes the notebook's own opening question rather
than a footnote about data availability. Restricting both languages to
exactly this 73-author intersection also fixes a real, if minor, flaw in
the chapter's own cross-language comparison: the book's own part-of-speech
proportion chart silently stacks all 75 English pages against only 73
French ones, while this notebook's version compares the identical
population on both sides. The corpus earns its second half of the notebook
independently of the population question, too. Running the same
`compute_tfidf` call the chapter uses for its own top-terms table
(`max_df=1.0`) turns up a real gap between the chapter's prose and its own
rendered output — English and French lists alike are dominated by function
words, not the names and titles the text promises — which only the
chapter's own stricter `max_df=0.5` (already used elsewhere in the same
chapter) actually fixes, and cleaning up to that standard is what surfaces
a genuine scraping artifact, leaked coordinate-template CSS, sitting in
exactly two English authors' pages and no French ones. The distance and
UMAP tools the chapter builds for a single language carry over to a
second one with no code changes at all, and applying them separately to
`anno_en` and `anno_fr` gives the closing sections of the chapter something
to measure that the chapter itself only gestures at: a 47.9% cross-lingual
nearest-neighbor agreement rate, far above chance but far from identical
geometry, standing in for the chapter's own closing paragraph about
projections that "differ" between editions.

Notebook42 stays on notebook41's exact 200-article AG News subsample rather
than drawing a fresh one, following the same logic notebook40 used to stay on
notebook39's IMDb subsample: 15.4–15.5's new material (document vectors,
UMAP, and angle distance) is a second pass over the same TF-IDF table
notebook41 already built, and the four disjoint `label` categories are
exactly what a chapter about telling documents apart needs. The dataset
earns the repeat on its own merits, too. The `olympic`/`profit` two-term
scatter that opens the chapter's own vector intuition lands on a cleaner
result here than the book's `poem`/`novel` example: zero AG News articles
score nonzero on both terms, against the book's authors who genuinely write
in both forms and populate the upper-right corner, because the topics behind
these two words are disjoint by construction where two literary forms are
not. The four-category structure also gives the UMAP and distance sections
something the book's single-subject author corpus cannot: a same-label
nearest-neighbor rate to measure instead of just eyeballing a plot, which
lands at 50% in the 2D projection and 70% in the full-dimensional distances,
both well above the 25% chance rate for four labels but well short of clean
separation, with `Sci/Tech` the hardest topic to keep together under both
methods and `Sports` the easiest. AG News also supplies a real instance of
exactly the failure the chapter warns about when it argues for angle
distance over Euclidean: two long, otherwise unremarkable articles get
picked as the raw Euclidean nearest neighbor for 136 of the 200 documents
(68%) regardless of topic, a concrete number no amount of warning about
document length could have supplied without a corpus containing both long
and short documents side by side. Reusing the same 200 articles also means
`anno` and the TF-IDF table do not need rebuilding from scratch, which was
notebook40's reason for reuse as well.

Notebook41 takes a 200-article subsample of AG News (50 each from
`Business`, `Sci/Tech`, `Sports`, and `World`, drawn deterministically from
the benchmark's held-out test partition) over the other text candidates
because chapter 15's new material — TF-IDF weighting, `min_df`/`max_df`
tuning, top terms per document — needs real, disjoint topic categories to
test itself against, and AG News is the only candidate in the text pool
that has them; the Wikipedia and IMDb corpora already spent on chapters 14
and 15's own examples are both single-subject by comparison. A raw
corpus-wide frequency count (question 1) has no dominant content word to
lean on at all, since the corpus mixes four unrelated subjects by design —
a sharper version of the chapter's own "publisher" point than IMDb could
give, since here TF-IDF is not just downweighting one recurring word but
the only thing that can separate the topics in the first place. The corpus
also earns the notebook a real, checkable stopword-tuning lesson the
chapter itself does not raise: pronouns and prepositions like `he`, `who`,
and `they` top out under 15% document frequency across the 200 articles
(question 6), so no `max_df` cutoff short of destroying real content words
ever removes them from a short document's own top-10 list (question 7),
unlike "publisher," which sits on almost every Wikipedia biography and
disappears cleanly. A genuine line-wrap artifact — a literal backslash
fusing two words with no space, inherited from the original AG News scrape
— sits in 23 of the 200 articles, concentrated in Business and absent from
Sports, and hands question 5 a deliberate failure with no authoring
required: every fused token is tagged non-alphabetic by spaCy, so it
silently disappears from every count in the notebook with no error raised
anywhere. Redefining the document unit as the category itself (question 8,
using `compute_tfidf`'s `doc_name` argument on a four-row pooled table)
turns the chapter's own throwaway line about how "the result depends on how
we define a document" into a concrete, checkable result, landing on real,
spot-checkable vocabulary (`IBM`, `Linux`, `olympic`, `Athens`, `Najaf`)
that traces back to real news from AG News's own 2004 collection window —
exactly the kind of check the notebook's own closing question asks for. AG
News is unused anywhere in either course's ledger.

Notebook40 stays on notebook39's exact 200-review IMDb subsample rather than
drawing a fresh one, because 14.5–14.10's new material — n-grams, named
entities, dependency parses, KWIC, and complexity metrics — is a second pass
over the same kind of pipeline output notebook39 already built, and the
`label` column keeps paying off the same way it did there. The dataset earns
the repeat rather than a swap on its own merits, too: `PERSON` entities in a
review corpus are a genuine mix of real people (directors, actors) and
fictional characters with nothing in the label to tell them apart, which the
biography corpus's own named entities never raise since every person on a
Wikipedia author's page is a real one; the dependency parse turns up 76
negated predicate adjectives, only 30 of them adjacent to their negation, a
concrete number no amount of warning about "not bad" could have supplied
without a corpus of first-person, negation-heavy prose behind it; and the
four complexity metrics the chapter introduces come back nearly identical
across `positive` and `negative` reviews, a genuinely negative result that
sends the closing question looking for a signal outside the chapter's own
toolkit (a plain count of `"!"` tokens) rather than manufacturing a positive
one where the data does not support it. Reusing the same 200 reviews also
means `anno` does not need re-annotating from scratch in the Setup block,
which keeps a twelve-question, five-section notebook inside the same
runtime budget as any single-topic one.

Notebook38 takes the keylog family, set aside for exactly this purpose when
notebook37 picked storms instead: `t0`/`t1` are milliseconds elapsed since
each of 823 recording sessions began, not a calendar timestamp, which rules
out `pl.date()`, weekday extraction, and time zones (13.1–13.6's material)
but is exactly the right shape for 13.7–13.11's truncation, window functions,
durations, and time-based rolling windows. The one real obstacle is that
`.dt.truncate()` and `.rolling_mean_by()` both require an actual `Datetime`
column, and `t0`/`t1` are plain floats. Casting them to `pl.Datetime("ms")`
solves this cleanly and honestly, because that is genuinely how a Unix
timestamp is stored: an integer count of milliseconds since a reference
moment. Anchoring at 1970-01-01 instead of session start turns out to be a
feature rather than a workaround, since every session shares the same
anchor, so truncating and pooling across all 823 sessions at once (question
2) reads as "everyone's Nth minute of typing," and the same sharing makes
question 9's `.over()` omission fail more dramatically than the chapter's
own warning describes: 393 unrelated sessions collide inside one session's
first 15 seconds of anchored time, not just the neighboring rows a plain
row-count window would blend. `keylog-meta.csv.gz` earns its place by
answering the question the catalogue itself poses for this dataset — how
L1 background and English proficiency show up in low-level typing rhythm —
with a real, monotonic result: average inter-key gap rises from 402 ms at
CEFR `C1/C2` to 586 ms at `B1/B2` to 667 ms at `A1/A2` (question 6). The
corpus also supplies its own deliberate-failure material with no authoring
needed: nobody in 1.14 million keystrokes ever presses a key before
releasing the last one (question 11's `.join_where()` interval check comes
back empty, confirmed cheaply corpus-wide by `gap`'s minimum), and a single
row out of 1.14 million, one pause lasting 42 minutes 57.8 seconds, is
enough to push its own typist to the third-highest average gap in the
study while barely moving the corpus mean (question 7). Both are checkable
outcomes the data already contains, not traps built in after the fact.

Notebook39 takes a 200-review subsample of the IMDb corpus (100 positive,
100 negative, selected deterministically so the notebook reruns the same way
every time) over the other text candidates because the chapter's own new
material in 14.1–14.4 is about building and trusting an annotation pipeline,
and IMDb is the one candidate in the text pool that is real, properly-cased
prose with a built-in `label` to group by, rather than a pre-tokenized or
lowercased benchmark. BBC's article text turned out to be lowercased with no
sentence-initial capitals at all, which would have quietly crippled the
POS tagger and (for notebook40) the entity recognizer without an error to
flag it, and SST's rows are single pre-tokenized excerpts with spaces
inserted before punctuation, not sentences a real tokenizer has ever seen.
IMDb reviews are ordinary scraped web prose instead, complete with a
`<br />` HTML artifact in over half the rows, which earned the notebook
its own deliberate-failure arc: question 2 shows a single dirty review
producing tokens like `movie.<br` tagged (inconsistently) as `NOUN`, and
question 11 closes the loop by showing that the corpus-wide noun counts for
`movie` and `film` are quietly wrong by 8 and 6 respectively if that HTML
is never cleaned, even though the top-10 list itself looks unchanged either
way. The `label` column also gave the adjective-frequency section a real,
checkable finding in place of the chapter's own per-document adjective
lists: `bad` splits sharply by sentiment (86 negative uses against 17
positive) while `good` barely does (80 against 65), a gap question 10 traces
back to negation, the same point the chapter's own introduction makes about
"not bad." IMDb is unused anywhere in either course's ledger, and pairing it
with notebook40 (14.5–14.10, which needs properly-cased text for named
entity recognition and dependency parsing even more than 14.1–14.4 does)
means both notebooks draw on the same corpus rather than one of them
inheriting a dataset picked for the other half's needs.

Notebook37 takes the storm family over the other temporal candidates because
the chapter's own new material — building a date from components, a
datetime with hour precision, and the naive/aware time-zone split — needs a
dataset with real, irregularly-timed events across real calendar dates, and
storms is the candidate in the pool that supplies all three without also
being the thin, hourly-but-only-one-year RVA/weather pair already spent by
notebook30's review, or the daily-only France/Italy COVID series that has no
hour component to build a datetime from at all. The six-hour observation
cadence (with genuine off-cycle fixes clustering around landfall) gives
question 7 a real, checkable gap to find, and NOAA's UTC convention gives
question 9 and 10 an actual reason to attach and convert a time zone rather
than doing it for its own sake. The dataset earns its deliberate failure on
its own, too, at no authoring cost: Atlantic storm names recycle every six
years, so `name == "Katrina"` alone pulls back three unrelated storms from
1981, 1999, and 2005, and a naive row-number plot stitches them into one
false continuous life cycle — the same not-a-key trap notebook35 hit with
Wikipedia disambiguation, recurring here for free because the data already
works that way, not because a trap was engineered. Keylog, the other strong
candidate the topic list flagged, was set aside for this notebook because
its `t0`/`t1` fields are session-relative milliseconds with no calendar date
behind them at all, which rules out `pl.date()`, weekday extraction, and
time zones — the entire content of 13.1–13.6 — even though it is exactly
the right shape for notebook38's durations and rolling windows.

Notebook35 does not draw from `dataset_description.qmd` at all, because chapter
12 is the one chapter in this range where avoiding the book's own dataset
means collecting a different one live rather than picking a different file
from the catalogue. The population is the direct membership of
`Category:Turing Award laureates`, the ACM's annual computing prize, which
Knuth's own collected article extract calls "informally considered the Nobel
Prize of computer science" — a fact the corpus hands back on its own once
collected, not something asserted in the notebook's prose. Eighty-one pages
as of collection, comfortably inside the "one sitting" budget the chapter's
politeness caution calls for, and small enough that notebook35 and notebook36
can both re-run from a cold cache in well under a minute of actual network
time. It earns the notebook on stronger grounds than convenience, though. A
single, official, well-maintained category with no subcategories to descend
into means the population question that opens the chapter has a clean
answer, which leaves the redirect and disambiguation material to carry the
notebook's real teaching weight: six of the eighty-one titles need a
Wikipedia disambiguator (`John McCarthy (computer scientist)`, `David
Patterson (computer scientist)`, and four more) because the plain name
belongs to someone else on Wikipedia, and typing the plain form for exactly
those two during collection resolves cleanly, with a real page ID and no
error, to a disambiguation page rather than a missing-page flag — a failure
mode the chapter's own redirect section does not surface with its own
population, since Victorian and Irish novelists rarely share a name with
someone more Wikipedia-famous. The corpus is unrelated to every dataset
already spent on either course (not `wiki_uk_*`, not English Wikipedia's link
graph, not SCOTUS), and it is the population notebook36 continues, since
collecting a second one for the links, revisions, page views, and language
links that chapter still owes would just mean re-running this same pipeline
for no pedagogical reason.

Notebook34 closes out the chapter-11 arc by pulling all three Italy tables
into one notebook, though `it_province_covid.csv` only lends its `region`
column this time rather than the daily case series. The pairing earns the
notebook because buffers, dissolving, exploding, and simplifying all need
something the earlier two Italy tables already supply on their own: buffers
reuse the city points and re-run the notebook33 spatial join under a changed
premise (containment versus proximity), and dissolving needs a real grouping
column richer than anything derivable from the polygons alone, which is
exactly what `region` on the covid table provides for free, 21 clean regions
with zero unmatched provinces. No new dataset was picked because the
province polygon file itself turns out to carry the deliberate-failure
material other datasets would need supplementing to provide: several
provinces are stored as genuine multi-part `MultiPolygon`s, and exploding
them lands on real, checkable places (Ischia, Capri, and Procida falling out
of Napoli in close-to-correct proportion to their known areas) right next to
a fake one (Trieste's 41 "parts," almost all sub-hectare slivers with no
actual island behind them), which is precisely the contrast a Best Practices
notebook about trusting-but-verifying spatial output needs, and reaching for
an unrelated table would have meant losing it.

Notebook33 puts the two Italy tables from the previous notebooks together,
because spatial joins are the one topic in this range that needs a point table
and a polygon table at once, and the family already carries both: `it_cities.csv`
(388 city points) and `it_province.geojson` (107 province polygons). The pairing
earns the notebook for four reasons. First, the containment join is clean and
complete: all 388 city points fall inside some province, so the point-in-polygon
`sjoin` returns 388 rows with nothing dropped, which lets the row-count-discipline
question resolve as a passing check while still teaching why the check exists
(a spatial inner join drops non-matches silently). Second, `it_cities.csv` has a
genuine data error the spatial join exposes for free: five names (Massa, Prato,
San Paolo, Vignola, Rovereto) repeat at different coordinates but with the *same*
population copied onto every duplicate, so a name join would cross-match them and
a spatial join sends each to its own province while the identical population column
flags the problem, which is exactly the "spot-check against something you know"
lesson. Third, province adjacency is real and checkable: the `touches` self-join
gives Milano its seven Lombard neighbors and leaves island/border provinces like
Cagliari and Trieste with a single land neighbor, both verifiable from a map rather
than asserted. Fourth, the nearest-neighbor section lands on island and mountain
towns (Olbia to Nuoro across Sardinia, Imperia to Cuneo over the Ligurian alps),
and the projected-versus-unprojected distance ranking actually flips at the top
(Imperia jumps to first in degrees), giving the deliberate-failure a checkable
reordering instead of a warning. No new dataset was picked because the point of
the notebook is joining the two tables the chapter's own units already gave us;
reaching for an unrelated table would break the "let the topic pick the dataset"
rule for the one notebook where the topic most needs these exact two.

Notebook32 stays inside the Italy family, as planned for all four chapter-11
notebooks, and moves from points to polygons: `it_province.geojson` (107
provinces, the `province` name plus a `MultiPolygon` geometry) carries the
Spatial Polygons and Polygon Metrics sections, and `it_province_covid.csv`
(daily new cases per province, Feb 2020–Nov 2021) supplies a real attribute to
color the Choropleth section. The pair earns the notebook for three reasons.
First, the two tables share a clean key: `province` is unique in both and the
107 names match exactly with no anti-join leftovers, so the join-key discipline
question resolves cleanly instead of turning into a name-cleaning detour that
belongs to an earlier chapter. Second, the province areas span two honest
orders of magnitude — rural Sassari (~7,700 km²) against urban Trieste
(~212 km²) — which makes the area-in-degrees failure obvious and gives the
"large regions dominate a choropleth" caution a concrete pair to point at.
Third, and the reason it beat a plain area map, the COVID totals invert under
area normalization: Naples is only third by raw total but first by cases per
km², and Sassari (largest by area) is nowhere near the top, so the
absolute-count-versus-density lesson lands as a checkable ranking flip rather
than an assertion. The provincial COVID table was preferred over reusing
`it_cities.csv` here because a choropleth wants a per-region quantity that
joins onto the polygons, not a scatter of city points, and it is otherwise
unused in either course.

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
