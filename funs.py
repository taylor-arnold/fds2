import numpy as np
import polars as pl
import plotnine as p9
import inspect
import pandas as pd
import geopandas as gpd
import shapely.wkt

p9.theme_set(p9.theme_minimal())


# ============================================================
# Polars display utility (ch03)
# ============================================================

def _patched_print(self, n=8):
    """Display a DataFrame showing a specific number of rows, as a terminal method in a chain."""
    with pl.Config(tbl_rows=n):
        try:
            # If running in a notebook, display the rich HTML table
            from IPython.display import display
            display(self)
        except ImportError:
            # Fallback for standard terminal environments
            print(self)

    # Returning None prevents Jupyter from double-printing
    # the dataframe if this is the last line in a cell.
    return None

pl.DataFrame.print = _patched_print


# ============================================================
# Plotnine x Polars integration (ch04, ch07)
# ============================================================
# Lets ggplot() accept a Polars DataFrame directly, applies a default
# categorical ordering to string columns, promotes WKT "geometry" columns
# to GeoPandas for geom_map(), supports `c.COLNAME` expressions inside
# aes(), and attaches every geom_/stat_/scale_/... component as a ggplot
# method so plots can be built as a single method chain.

_orig_ggplot_init = p9.ggplot.__init__
_orig_geom_map_init = p9.geom_map.__init__

def _prepare_plot_data(df):
    """Apply categorical ordering to strings and convert WKT geometries to GeoPandas."""
    if not isinstance(df, pl.DataFrame):
        return df

    # Categorical logic
    string_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.String]
    if string_cols:
        exprs = []
        for col in string_cols:
            if col == "geometry":
                continue
            unique_vals = df[col].unique(maintain_order=True).drop_nulls().to_list()
            exprs.append(pl.col(col).cast(pl.Enum(unique_vals)))
        if exprs:
            df = df.with_columns(exprs)

    # Geometry logic
    if "geometry" in df.columns:
        pdf = df.to_pandas()
        pdf["geometry"] = pdf["geometry"].apply(
            lambda x: shapely.wkt.loads(x) if isinstance(x, str) and pd.notnull(x) else x
        )
        return gpd.GeoDataFrame(pdf, geometry="geometry")

    return df

def _patched_ggplot_init(self, *args, **kwargs):
    new_args = list(args)
    if len(args) > 0 and isinstance(args[0], pl.DataFrame):
        new_args[0] = _prepare_plot_data(args[0])
    elif 'data' in kwargs:
        kwargs['data'] = _prepare_plot_data(kwargs['data'])
    _orig_ggplot_init(self, *new_args, **kwargs)

def _patched_geom_map_init(self, *args, **kwargs):
    new_args = list(args)
    # geom_map often receives data as the second positional argument
    if len(args) > 1 and isinstance(args[1], pl.DataFrame):
        new_args[1] = _prepare_plot_data(args[1])
    elif 'data' in kwargs:
        kwargs['data'] = _prepare_plot_data(kwargs['data'])
    _orig_geom_map_init(self, *new_args, **kwargs)

p9.ggplot.__init__ = _patched_ggplot_init
p9.geom_map.__init__ = _patched_geom_map_init

def _extract_names(val):
    """Recursively pull the string column name out of `c.COLNAME`-style Polars expressions."""
    if isinstance(val, pl.Expr):
        return val.meta.output_name()
    elif isinstance(val, (list, tuple)):
        # Handle lists of expressions like [c.id, c.date]
        return [_extract_names(v) for v in val]
    elif isinstance(val, dict):
        return {k: _extract_names(v) for k, v in val.items()}
    return val

_orig_aes_init = p9.aes.__init__

def _patched_aes_init(self, *args, **kwargs):
    """Wrap aes() so it accepts `c.COLNAME` expressions in place of column-name strings."""
    new_args = tuple(_extract_names(arg) for arg in args)
    new_kwargs = {k: _extract_names(v) for k, v in kwargs.items()}
    _orig_aes_init(self, *new_args, **new_kwargs)

p9.aes.__init__ = _patched_aes_init

# Dynamically attach every geom_/stat_/theme/scale_/facet_/coord_/guides/labs/
# annotate component to the ggplot class as a method, so that
# ggplot(...).geom_point() runs ggplot(...) + geom_point() behind the scenes.
_component_prefixes = ('geom_', 'stat_', 'theme', 'scale_', 'facet_', 'coord_', 'guides', 'labs', 'annotate')

for _name in dir(p9):
    _obj = getattr(p9, _name)
    if inspect.isclass(_obj) and _name.startswith(_component_prefixes):

        def _make_method(component_cls):
            def method(self, *args, **kwargs):
                return self + component_cls(*args, **kwargs)
            return method

        setattr(p9.ggplot, _name, _make_method(_obj))

# theme() and guides() need more than a plain method. ggplot.__init__ stores a
# component of each of those names on the instance (self.theme = theme_get(),
# self.guides = guides()), and an instance attribute hides a class method of the
# same name, so the methods attached above are unreachable for these two. A data
# descriptor, however, takes precedence over the instance dictionary. Each one
# below hands plotnine back the component it stored, so `plot.theme` keeps
# working internally, and records the plot the component came from so that
# *calling* the component adds a fresh one to that plot. The owner is recorded as
# .plot, the name plotnine itself uses (theme.setup) and the one its __deepcopy__
# knows not to follow.

def _make_chainable_component(name):
    component_cls = getattr(p9, name)
    store = f"_{name}"

    class _ChainableComponent:
        def __get__(self, plot, owner=None):
            if plot is None:
                return self
            try:
                component = plot.__dict__[store]
            except KeyError:
                raise AttributeError(name) from None
            component.plot = plot
            return component

        def __set__(self, plot, component):
            plot.__dict__[store] = component

    def _call(self, *args, **kwargs):
        plot = getattr(self, "plot", None)
        if plot is None:
            raise TypeError(f"{name}() is only callable as a method of a ggplot object")
        return plot + component_cls(*args, **kwargs)

    component_cls.__call__ = _call
    setattr(p9.ggplot, name, _ChainableComponent())

for _name in ('theme', 'guides'):
    _make_chainable_component(_name)


# ============================================================
# Reshaping (ch09)
# ============================================================
# Lets .pivot() and .unpivot() accept `c.COLNAME` expressions in place of
# column-name strings, reusing the _extract_names() helper defined above.

_orig_pivot = pl.DataFrame.pivot
_orig_unpivot = pl.DataFrame.unpivot

def _patched_pivot(self, *args, **kwargs):
    """Wrap .pivot() so it accepts `c.COLNAME` expressions in place of column-name strings."""
    new_args = tuple(_extract_names(arg) for arg in args)
    new_kwargs = {k: _extract_names(v) for k, v in kwargs.items()}
    return _orig_pivot(self, *new_args, **new_kwargs)

def _patched_unpivot(self, *args, **kwargs):
    """Wrap .unpivot() so it accepts `c.COLNAME` expressions in place of column-name strings."""
    new_args = tuple(_extract_names(arg) for arg in args)
    new_kwargs = {k: _extract_names(v) for k, v in kwargs.items()}
    return _orig_unpivot(self, *new_args, **new_kwargs)

pl.DataFrame.pivot = _patched_pivot
pl.DataFrame.unpivot = _patched_unpivot


# ============================================================
# Spatial data (ch11)
# ============================================================

@pl.api.register_dataframe_namespace("geo")
class GeoNamespace:
    """Seamless wrapper to run GeoPandas methods directly on Polars DataFrames."""

    def __init__(self, df: pl.DataFrame):
        self._df = df

    def _to_gdf(self):
        pdf = self._df.to_pandas()
        if "geometry" in pdf.columns:
            pdf["geometry"] = pdf["geometry"].apply(
                lambda x: shapely.wkt.loads(x) if isinstance(x, str) and pd.notnull(x) else x
            )
            gdf = gpd.GeoDataFrame(pdf, geometry="geometry")

            # Restore the CRS if we stashed it previously
            if "_crs" in gdf.columns:
                crs_val = gdf["_crs"].iloc[0]
                gdf = gdf.set_crs(crs_val).drop(columns=["_crs"])
            return gdf
        return gpd.GeoDataFrame(pdf)

    def _to_pl(self, obj):
        if isinstance(obj, (gpd.GeoDataFrame, pd.DataFrame)):
            # Promote meaningful indexes (e.g. the group keys created by
            # .dissolve or .groupby) to regular columns so they survive the
            # conversion back to Polars, which drops the pandas index.
            if obj.index.name is not None or isinstance(obj.index, pd.MultiIndex):
                obj = obj.reset_index()

            # Stash the CRS into a string column before converting back
            if hasattr(obj, "crs") and obj.crs is not None:
                obj["_crs"] = obj.crs.to_string()

            if "geometry" in obj.columns:
                obj["geometry"] = obj["geometry"].apply(
                    lambda x: x.wkt if pd.notnull(x) else None
                )
            return pl.from_pandas(pd.DataFrame(obj))
        return obj

    def _wrap_result(self, name, result):
        """Convert a GeoPandas result back into the Polars world."""
        if isinstance(result, gpd.GeoSeries):
            # Overwrite 'geometry' column with new geometries (e.g., .buffer, .centroid)
            wkt_series = result.apply(lambda x: x.wkt if pd.notnull(x) else None)
            return self._df.with_columns(pl.Series("geometry", wkt_series))

        elif isinstance(result, pd.Series):
            # Append standard properties as a new column (e.g., .area)
            return self._df.with_columns(pl.Series(name, result))

        # GeoDataFrames (like .to_crs, .sjoin) and scalars pass through normally
        return self._to_pl(result)

    def points_from_xy(self, x="lon", y="lat", crs=4326):
        """Build a point 'geometry' column from two coordinate columns and record the CRS.

        Defined explicitly because gpd.points_from_xy is a module-level
        function rather than a GeoDataFrame method.
        """
        pdf = self._df.to_pandas()
        gdf = gpd.GeoDataFrame(
            pdf, geometry=gpd.points_from_xy(pdf[x], pdf[y]), crs=crs
        )
        return self._to_pl(gdf)

    def __getattr__(self, name):
        """Intercept any GeoPandas method or property and handle the round-trip conversion."""
        # Properties such as .area, .centroid, and .crs are not callable, so we
        # evaluate them right away instead of returning a wrapper function.
        gdf = self._to_gdf()
        # Some properties (e.g. .x, .y, .z) live only on GeoSeries and are not
        # proxied onto GeoDataFrame, so fall back to the active geometry
        # column when the attribute isn't found directly on the frame.
        source = gdf if hasattr(gdf, name) else gdf.geometry
        attr = getattr(source, name)
        if not callable(attr):
            return self._wrap_result(name, attr)

        def wrapper(*args, **kwargs):
            # Convert any Polars dataframe arguments to GeoPandas
            new_args = [
                arg.geo._to_gdf() if isinstance(arg, pl.DataFrame) and "geometry" in arg.columns else arg
                for arg in args
            ]
            new_kwargs = {
                k: (v.geo._to_gdf() if isinstance(v, pl.DataFrame) and "geometry" in v.columns else v)
                for k, v in kwargs.items()
            }

            # Execute the GeoPandas method
            func = getattr(source, name)
            result = func(*new_args, **new_kwargs)
            return self._wrap_result(name, result)

        return wrapper


def read_file(path, **kwargs):
    """Read any spatial file (GeoJSON, Shapefile, GeoPackage, ...) into a Polars DataFrame.

    Geometries are stored as WKT strings and the CRS is stashed in a
    '_crs' column so the geo namespace can restore it later.
    """
    gdf = gpd.read_file(path, **kwargs)
    pdf = pd.DataFrame(gdf)
    if gdf.crs is not None:
        pdf["_crs"] = gdf.crs.to_string()
    if "geometry" in pdf.columns:
        pdf["geometry"] = pdf["geometry"].apply(
            lambda x: x.wkt if pd.notnull(x) else None
        )
    return pl.from_pandas(pdf)


# ============================================================
# Text (ch13, ch14)
# ============================================================

class DSText:
    """Static helpers for turning raw text into an annotated token table and text-analysis features."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("DSText is a static utility class and cannot be instantiated")

    @staticmethod
    def process(docs_df, nlp):
        """Run a spaCy pipeline over each document and return one row per token."""
        tokens_list = []

        for row in docs_df.iter_rows(named=True):
            doc_id = row["doc_id"]
            text = row["text"]
            doc = nlp(text)

            sent_id = 0

            for sent in doc.sents:
                sent_id += 1
                sent_start = sent.start  # doc-global start offset for this sentence

                for token in sent:
                    tid = (token.i - sent_start) + 1  # 1-based within sentence

                    # head index in the SAME coordinate system as tid
                    if token.head == token:  # root
                        head_tid = tid
                    else:
                        head_tid = (token.head.i - sent_start) + 1

                    tokens_list.append({
                        "doc_id": doc_id,
                        "sid": sent_id,
                        "tid": tid,
                        "token": token.text,
                        "token_with_ws": token.text_with_ws,
                        "lemma": token.lemma_,
                        "upos": token.pos_,
                        "tag": token.tag_,
                        "is_alpha": token.is_alpha,
                        "is_stop": token.is_stop,
                        "is_punct": token.is_punct,
                        "dep": token.dep_,
                        "head_idx": head_tid,
                        "ent_type": token.ent_type_,
                        "ent_iob": token.ent_iob_,
                    })

        return pl.DataFrame(tokens_list)

    @staticmethod
    def compute_tfidf(df, min_df=0.0, max_df=1.0, doc_name="doc_id"):
        """Compute TF-IDF weights for each (document, lemma) pair.

        min_df / max_df are proportions in [0, 1], e.g. max_df=0.5 keeps
        terms occurring in <= 50% of documents.
        """
        n_docs = df.select(pl.col(doc_name).n_unique()).item()

        tfidf = (
            df
            .filter(pl.col("is_alpha"))
            .group_by([doc_name, "lemma"])
            .agg(tf=pl.len())
            .with_columns(
                tf_norm=pl.col("tf") / pl.col("tf").sum().over(doc_name),
            )
            .with_columns(
                df_docs=pl.col(doc_name).n_unique().over("lemma"),
            )
            .with_columns(
                df_prop=pl.col("df_docs") / pl.lit(n_docs),
            )
            .filter(
                (pl.col("df_prop") >= pl.lit(min_df)) &
                (pl.col("df_prop") <= pl.lit(max_df))
            )
            .with_columns(
                idf=((pl.lit(n_docs) + 1) / (pl.col("df_docs") + 1)).log() + 1,
            )
            .with_columns(
                tfidf=pl.col("tf_norm") * pl.col("idf"),
            )
            .drop("df_prop")
        )

        return tfidf

    @staticmethod
    def compute_distances(df, min_df=0.0, max_df=1.0, doc_name="doc_id"):
        """Compute the pairwise angle distance between every pair of documents' TF-IDF vectors.

        min_df / max_df are proportions in [0, 1] and are passed through to compute_tfidf.
        """
        mat = (
            DSText.compute_tfidf(df, min_df=min_df, max_df=max_df, doc_name=doc_name)
            .pivot(on="lemma", index=doc_name, values="tfidf")
            .fill_null(0)
            .sort(doc_name)
        )

        doc_ids = mat.select(doc_name).to_series().to_list()

        X = mat.drop(doc_name).to_numpy()
        X = X / np.linalg.norm(X, axis=1, keepdims=True)
        angles = np.arccos(np.clip(X @ X.T, 0, 1))

        doc2_name = f"{doc_name}2"

        return (
            pl.DataFrame(angles, schema=[str(d) for d in doc_ids])
            .with_columns(pl.Series(doc_name, doc_ids))
            .unpivot(index=doc_name, variable_name=doc2_name, value_name="distance")
            .filter(pl.col(doc_name) < pl.col(doc2_name))
            .sort([doc_name, doc2_name])
        )

    @staticmethod
    def kwic(tokens, keyword, max_num=10, window=5, left_width=40, right_width=40):
        """Print a keyword-in-context display for each occurrence of `keyword`."""
        keyword = keyword.lower()

        prefix_width = (
            tokens
            .select(pl.col("doc_id").cast(pl.Utf8).str.len_chars().max())
            .item()
            + 6
        )

        matches = tokens.filter(pl.col("lemma") == keyword)
        if len(matches) > max_num:
            matches = matches[:max_num]

        for row in matches.iter_rows(named=True):
            doc = row["doc_id"]
            sid = row["sid"]
            tid = row["tid"]

            context = (
                tokens
                .filter(
                    (pl.col("doc_id") == doc) &
                    (pl.col("sid") == sid) &
                    (pl.col("tid") >= tid - window) &
                    (pl.col("tid") <= tid + window)
                )
                .sort("tid")
            )

            left = (
                context
                .filter(pl.col("tid") < tid)
                .select("token")
                .to_series()
                .to_list()
            )
            right = (
                context
                .filter(pl.col("tid") > tid)
                .select("token")
                .to_series()
                .to_list()
            )

            left_text = " ".join(left)[-left_width:]
            right_text = " ".join(right)[:right_width]

            prefix = f"{doc}:{sid}"

            print(
                f"{prefix:<{prefix_width}} "
                f"{left_text:>{left_width}} "
                f"[{row['token']}] "
                f"{right_text:<{right_width}}"
            )


# ============================================================
# Dimensionality reduction (ch14, ch16)
# ============================================================

def _extract_features(df, features, drop):
    """Select feature columns from `df` and return them as a NumPy array plus column names."""
    if features is not None:
        X_df = df.select(features)
    elif drop is not None:
        exclude = set(df.select(drop).columns)
        X_df = df.select([col for col in df.columns if col not in exclude])
    else:
        X_df = df

    if len(X_df.columns) == 1:
        col_dtype = X_df.dtypes[0]
        if isinstance(col_dtype, (pl.List, pl.Array)):
            X = np.vstack(X_df.to_series().to_list())
            n_cols = X.shape[1]
            pad_width = len(str(n_cols - 1))
            column_names = [f"col{str(i).zfill(pad_width)}" for i in range(n_cols)]
        else:
            column_names = X_df.columns
            X = X_df.to_numpy()
    else:
        column_names = X_df.columns
        X = X_df.to_numpy()

    return X, column_names


def umap(df, features=None, drop=None, **kwargs):
    """Fit UMAP on the selected feature columns of `df`."""
    X, column_names = _extract_features(df, features, drop)
    return _fit_umap(X, df, column_names, **kwargs)


def _build_dtm(df, doc_id, term_id, count=None, max_vocab_size=None, min_df=0.0, max_df=1.0):
    """Build a document-term matrix of TF-IDF weights.

    min_df / max_df are proportions in [0, 1] (document frequency fraction).
    """
    doc_col = df.select(doc_id).columns[0]
    term_col = df.select(term_id).columns[0]

    if count is not None:
        count_col = df.select(count).columns[0]
        dtm_df = df.select([doc_col, term_col, count_col])
    else:
        count_col = "_count_"
        dtm_df = df.select([doc_col, term_col]).with_columns(pl.lit(1).alias(count_col))

    # Stable doc index
    unique_docs = dtm_df.select(doc_col).unique().sort(doc_col)
    doc_ids = unique_docs.to_series().to_list()
    n_docs = len(doc_ids)

    if n_docs == 0:
        raise ValueError("No documents found.")

    # Document frequency per term (how many docs contain the term)
    term_doc_counts = (
        dtm_df
        .select([doc_col, term_col])
        .unique()
        .group_by(term_col)
        .agg(pl.len().alias("df_docs"))
        .with_columns((pl.col("df_docs") / pl.lit(n_docs)).alias("df_prop"))
    )

    # Apply df proportion filters
    valid_terms = term_doc_counts.filter(
        (pl.col("df_prop") >= pl.lit(min_df)) & (pl.col("df_prop") <= pl.lit(max_df))
    )

    # Optional vocab cap by df (common heuristic); you can switch to other criteria if preferred
    if max_vocab_size is not None and valid_terms.height > max_vocab_size:
        valid_terms = valid_terms.sort("df_docs", descending=True).head(max_vocab_size)

    valid_term_set = set(valid_terms.select(term_col).to_series().to_list())

    dtm_df = dtm_df.filter(pl.col(term_col).is_in(valid_term_set))

    # Stable term index
    unique_terms = dtm_df.select(term_col).unique().sort(term_col)
    term_names = unique_terms.to_series().to_list()
    n_terms = len(term_names)

    if n_terms == 0:
        raise ValueError("No terms remaining after applying min_df and max_df filters.")

    doc_to_idx = {doc: idx for idx, doc in enumerate(doc_ids)}
    term_to_idx = {term: idx for idx, term in enumerate(term_names)}

    # Aggregate counts per (doc, term)
    aggregated = (
        dtm_df
        .group_by([doc_col, term_col])
        .agg(pl.col(count_col).sum().alias("tf"))
    )

    # Compute normalized tf per doc
    aggregated = aggregated.with_columns(
        (pl.col("tf") / pl.col("tf").sum().over(doc_col)).alias("tf_norm")
    )

    # Join df_docs (document frequency) onto aggregated
    aggregated = aggregated.join(
        valid_terms.select([term_col, "df_docs"]),
        on=term_col,
        how="inner",
    )

    # Compute smoothed idf and tf-idf
    aggregated = aggregated.with_columns(
        (((pl.lit(n_docs) + 1) / (pl.col("df_docs") + 1)).log() + 1).alias("idf")
    ).with_columns(
        (pl.col("tf_norm") * pl.col("idf")).alias("tfidf")
    )

    # Build sparse matrix from tfidf weights
    rows, cols, data = [], [], []
    for row in aggregated.select([doc_col, term_col, "tfidf"]).iter_rows(named=True):
        doc = row[doc_col]
        term = row[term_col]
        val = float(row["tfidf"])

        # Guard (should always be true)
        if doc in doc_to_idx and term in term_to_idx:
            rows.append(doc_to_idx[doc])
            cols.append(term_to_idx[term])
            data.append(val)

    from scipy.sparse import csr_matrix

    sparse_matrix = csr_matrix((data, (rows, cols)), shape=(n_docs, n_terms))
    X = sparse_matrix.toarray()
    X = X / np.linalg.norm(X, axis=1, keepdims=True)

    return X, doc_ids, term_names


def umap_text(df, doc_id, term_id, count=None, max_vocab_size=None, min_df=0, max_df=1, **kwargs):
    """Build a TF-IDF document-term matrix from `df` and fit UMAP on it."""
    X, doc_ids, term_names = _build_dtm(df, doc_id, term_id, count, max_vocab_size, min_df, max_df)
    doc_col = df.select(doc_id).columns[0]
    doc_df = pl.DataFrame({doc_col: doc_ids})
    column_names = [str(t) for t in term_names]
    return _fit_umap(X, doc_df, column_names, **kwargs)


def _fit_umap(X, df, column_names, **kwargs):
    """Standardize `X` and fit UMAP on it, returning a UMAPResult."""
    from sklearn.preprocessing import StandardScaler
    import umap

    X_scaled = StandardScaler().fit_transform(X)
    model = umap.UMAP(**kwargs)
    embedding = model.fit_transform(X_scaled)

    return UMAPResult(model=model, df=df, column_names=column_names, embedding=embedding)


class UMAPResult:
    """The fitted UMAP model plus the embedding, with a .predict() method to retrieve the coordinates."""

    def __init__(self, model, df, column_names, embedding):
        self.model = model
        self.df = df
        self.column_names = column_names
        self.embedding = embedding

    def predict(self, prefix="dr", array=False, full=False):
        """Return the embedding as a Polars DataFrame, optionally joined back onto the source table."""
        data = {}
        if array:
            data[prefix] = self.embedding.tolist()
            result = pl.DataFrame(data).cast({prefix: pl.Array(pl.Float64, self.embedding.shape[1])})
        else:
            n_components = self.embedding.shape[1]
            pad_width = len(str(n_components - 1))
            for i in range(n_components):
                col_name = f"{prefix}{str(i).zfill(pad_width)}"
                data[col_name] = self.embedding[:, i].tolist()
            result = pl.DataFrame(data)

        if full:
            return pl.concat([self.df, result], how="horizontal")
        return result


# ============================================================
# Image (ch16)
# ============================================================

def dot_product(a, b):
    """Row-wise dot product of two list-typed Polars columns."""
    return (a * b).list.sum()


class DSImage:
    """Static helpers for summarizing and displaying image datasets."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("DSImage is a static utility class and cannot be instantiated")

    @staticmethod
    def compute_colors(img_hsv):
        """Return the percentage of pixels in an HSV image falling into each named hue bucket."""
        import cv2
        h, s, v = cv2.split(img_hsv)
        valid = (s >= 50) & (v >= 50)

        color_ranges = {
            'red': ((h <= 10) | (h >= 170)) & valid,
            'orange': (h > 10) & (h <= 25) & valid,
            'yellow': (h > 25) & (h <= 35) & valid,
            'green': (h > 35) & (h <= 85) & valid,
            'cyan': (h > 85) & (h <= 100) & valid,
            'blue': (h > 100) & (h <= 130) & valid,
            'purple': (h > 130) & (h <= 145) & valid,
            'magenta': (h > 145) & (h < 170) & valid,
        }

        total_pixels = img_hsv.shape[0] * img_hsv.shape[1]

        percentages = {color: np.sum(mask) / total_pixels * 100
                       for color, mask in color_ranges.items()}

        percentages['neutral'] = np.sum(~valid) / total_pixels * 100
        return percentages

    @staticmethod
    def plot_image_grid(df, ncol=10, label_name="label", filepath="filepath", limit=100):
        """Display up to `limit` images from `df` in a grid, labeled from `label_name` if present."""
        import matplotlib.pyplot as plt
        from PIL import Image
        import math

        df = df.head(limit)
        n = df.height
        if n == 0:
            return

        nrow = math.ceil(n / ncol)

        paths = df.select(filepath).to_series().to_list()
        labels = None
        if label_name is not None and label_name in df.columns:
            labels = df.select(label_name).to_series().to_list()

        fig, axes = plt.subplots(nrow, ncol, figsize=(ncol * 2, nrow * 2))
        axes = np.array(axes).ravel()

        for i, ax in enumerate(axes):
            if i < n:
                img = Image.open(paths[i])
                cmap = "gray" if img.mode == "L" else None
                ax.imshow(img, cmap=cmap)

                if labels is not None:
                    ax.set_title(str(labels[i]), fontsize=8)

                w, h = img.size
                max_dim = max(h, w)
                ax.set_xlim(-0.5 + (w - max_dim) / 2, w - 0.5 + (max_dim - w) / 2)
                ax.set_ylim(h - 0.5 + (max_dim - h) / 2, -0.5 + (h - max_dim) / 2)
                ax.set_aspect("equal")
                ax.axis("off")
            else:
                ax.axis("off")

        fig.set_constrained_layout(True)
        plt.show()


class ViTEmbedder:
    """Wraps a Vision Transformer (ViT) model to embed images as fixed-length vectors."""

    def __init__(self, model_name="google/vit-base-patch16-224", pooling="mean"):
        from transformers import AutoImageProcessor, ViTModel
        import torch

        self.pooling = pooling.lower()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
        self.model = ViTModel.from_pretrained(model_name, add_pooling_layer=False).eval().to(self.device)

    def __call__(self, image_path):
        """Embed the image at `image_path` and return it as a NumPy vector."""
        import torch
        from PIL import Image

        with torch.inference_mode():
            inputs = {k: v.to(self.device) for k, v in self.processor(images=Image.open(image_path).convert("RGB"), return_tensors="pt").items()}
            hidden = self.model(**inputs).last_hidden_state
            vec = torch.nn.functional.normalize(hidden[:, 0, :] if self.pooling == "cls" else hidden[:, 1:, :].mean(dim=1), p=2, dim=-1)
            return vec.squeeze(0).cpu().numpy()


class SigLIPEmbedder:
    """Wraps a SigLIP model to embed images and text into a shared vector space."""

    def __init__(self, model_name="google/siglip-base-patch16-256", device=None):
        from transformers import AutoProcessor, SiglipModel
        import torch

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)
        self.model = SiglipModel.from_pretrained(model_name).eval().to(self.device)

    def embed_image(self, image_path):
        """Embed the image at `image_path` and return it as a NumPy vector."""
        import torch
        from PIL import Image

        with torch.inference_mode():
            inputs = self.processor(images=Image.open(image_path).convert("RGB"), return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            vec = torch.nn.functional.normalize(self.model.get_image_features(**inputs).pooler_output, p=2, dim=-1)
            return vec.squeeze(0).cpu().numpy()

    def embed_text(self, text):
        """Embed `text` and return it as a NumPy vector in the same space as embed_image()."""
        import torch

        with torch.inference_mode():
            inputs = self.processor(text=text, return_tensors="pt", padding="max_length")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            vec = torch.nn.functional.normalize(self.model.get_text_features(**inputs).pooler_output, p=2, dim=-1)
            return vec.squeeze(0).cpu().numpy()


# ============================================================
# Network (ch15)
# ============================================================

class DSNetwork:
    """Static helpers for turning an edge table into a laid-out, metric-annotated graph."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("DSNetwork is a static utility class and cannot be instantiated")

    @staticmethod
    def process(edges_df, directed=False):
        """Build a graph from an edge table and return (node_df, edge_df, graph).

        node_df and edge_df carry a Fruchterman-Reingold layout plus, per node,
        connected-component membership, a community label, and degree/eigenvector/
        betweenness/closeness centrality scores (closeness only when undirected).
        """
        import igraph as ig

        if isinstance(edges_df, pl.DataFrame):
            edge_list = [
                (row["doc_id"], row["doc_id2"])
                for row in edges_df.iter_rows(named=True)
            ]
        else:
            edge_list = [
                (row["doc_id"], row["doc_id2"])
                for _, row in edges_df.iterrows()
            ]

        G = ig.Graph.TupleList(edge_list, directed=directed)
        layout = G.layout_fruchterman_reingold()
        components = G.connected_components()
        clusters = G.community_walktrap().as_clustering().membership

        vertex_names = [v["name"] for v in G.vs]
        name_to_idx = {name: i for i, name in enumerate(vertex_names)}

        nodes = []
        for i, vertex in enumerate(G.vs):
            component_id = None
            for comp_idx, component in enumerate(components):
                if i in component:
                    component_id = comp_idx + 1
                    break

            node_data = {
                "id": vertex["name"],
                "x": layout[i][0],
                "y": layout[i][1],
                "component": component_id,
                "component_size": len(components[component_id - 1]) if component_id else 0,
                "cluster": str(clusters[i])
            }

            if directed:
                node_data.update({
                    "degree_out": vertex.outdegree(),
                    "degree_in": vertex.indegree(),
                    "degree_total": vertex.degree()
                })
            else:
                node_data["degree"] = vertex.degree()

            nodes.append(node_data)

        eigen_vals = [None] * len(G.vs)
        between_vals = [None] * len(G.vs)
        close_vals = [None] * len(G.vs) if not directed else None

        for comp_idx, component in enumerate(components):
            if len(component) > 1:
                subgraph = G.subgraph(component)
                sub_names = [v["name"] for v in subgraph.vs]

                eigen_scores = subgraph.eigenvector_centrality()
                between_scores = subgraph.betweenness(directed=directed)

                for sub_i, name in enumerate(sub_names):
                    main_i = name_to_idx[name]
                    eigen_vals[main_i] = eigen_scores[sub_i]
                    between_vals[main_i] = between_scores[sub_i]

                if not directed:
                    # Sum of the reciprocals of the shortest-path distances, which is
                    # igraph's harmonic centrality. Not igraph's closeness(), which is
                    # (n - 1) / sum(d) and ranks bridge nodes differently.
                    close_scores = subgraph.harmonic_centrality(normalized=False)
                    for sub_i, name in enumerate(sub_names):
                        main_i = name_to_idx[name]
                        close_vals[main_i] = close_scores[sub_i]

        for i, node in enumerate(nodes):
            node["eigen"] = eigen_vals[i]
            node["between"] = between_vals[i]
            if not directed:
                node["close"] = close_vals[i]

        node_df = pl.DataFrame(nodes)

        edges_plot = []
        for edge in G.es:
            source_idx = edge.source
            target_idx = edge.target
            edges_plot.append({
                "x": layout[source_idx][0],
                "y": layout[source_idx][1],
                "xend": layout[target_idx][0],
                "yend": layout[target_idx][1]
            })

        edge_df = pl.DataFrame(edges_plot)

        return node_df, edge_df, G
