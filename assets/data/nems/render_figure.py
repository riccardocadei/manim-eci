"""
Render s18 Figure frame sequences (2x3 subplots) for multi-phase animated
reveal in Manim. Mirrors the s09 pattern in assets/data/experiment/render_figure5.py.

Phases:
  1. grow_base_XX.png   — t-test + Bonferroni bars grow (NEMS hidden)
  2. trend.png          — same + red trend line on precision showing the paradox
  3. add_nems_XX.png    — baselines dimmed, NEMS (ours) grows in
  + figure_full.png     — final static (all 3 methods full)

Data:
  effect_sweep.parquet   — varying effect size η (fixed n = 500)
  n_sweep.parquet        — varying sample size n (fixed η = 5)

Methods kept (others ignored per request):
  Marginal        → "t-test"
  Marginal (Bon)  → "Bonferroni"
  NEMS (auto)     → "NEMS (ours)"

Error bars: 95% CI across seeds (1.96 × SEM).
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(HERE, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

EFFECT_PATH = os.path.join(HERE, "effect_sweep.parquet")
N_PATH      = os.path.join(HERE, "n_sweep.parquet")

# ── Dark theme (match s09) ──
BG      = "#000000"
TXT     = "#F2F2F2"
GRID_C  = "#333333"
SPINE_C = "#555555"
BAR_E   = "#222222"

# 3 methods, in bar order (baselines first, NEMS last/right)
METHODS = [
    ("Marginal",       "#E07A5F", r"$t$-test"),
    ("Marginal (Bon)", "#81B29A", "Bonferroni"),
    ("NEMS (auto)",    "#5BC4F5", "NEMS (ours)"),
]
NEMS_METHOD   = METHODS[2]
BASELINES     = METHODS[:2]
BASELINE_KEYS = {m[0] for m in BASELINES}
NEMS_KEYS     = {NEMS_METHOD[0]}

METRICS = [
    ("precision", "Precision"),
    ("recall",    "Recall"),
    ("iou",       "IoU"),
]

# Data filters (per user request)
FIXED_N      = 500
FIXED_EFFECT = 5.0

# Ticks (subset of available values, for bar-chart clarity)
N_TICKS   = [50, 500, 2000, 10000]
ETA_TICKS = [2, 4, 6, 10]

N_FRAMES = 15


def _load_data():
    df_e = pd.read_parquet(EFFECT_PATH)
    df_e = df_e[df_e.fixed_n == FIXED_N].copy()
    df_n = pd.read_parquet(N_PATH)
    df_n = df_n[df_n.fixed_effect == FIXED_EFFECT].copy()
    return df_e, df_n


def _stats(df, x_col, x_values, method_key, metric):
    means, cis = [], []
    for xv in x_values:
        sub = df[(df[x_col] == xv) & (df.method == method_key)][metric]
        if len(sub) == 0:
            means.append(0.0); cis.append(0.0)
        else:
            means.append(float(sub.mean()))
            sem = float(sub.std(ddof=1)) / np.sqrt(len(sub))
            cis.append(1.96 * sem)  # 95% CI half-width
    return np.array(means), np.array(cis)


def ease_out(t):
    return 1.0 - (1.0 - t) ** 2.5


def plot_bars_on_ax(ax, df, x_axis_col, x_values, metric_key,
                    height_scale=None, dim_keys=None, hide_keys=None,
                    draw_trend=False):
    if height_scale is None: height_scale = {}
    if dim_keys is None:     dim_keys = set()
    if hide_keys is None:    hide_keys = set()

    G = len(x_values)
    M = len(METHODS)
    idx = np.arange(G, dtype=float)
    width = min(0.8 / max(M, 1), 0.24)
    offsets = (np.arange(M) - (M - 1) / 2.0) * (width + 0.03)

    # Collect visible bar means for trend line (same policy as s09)
    trend_means_per_x = [[] for _ in range(G)]

    for j, (key, color, alias) in enumerate(METHODS):
        if key in hide_keys:
            continue
        s = height_scale.get(key, 1.0)
        means, cis = _stats(df, x_axis_col, x_values, key, metric_key)
        means = means * s
        cis   = cis   * s
        x_centers = idx + offsets[j]

        is_dim = key in dim_keys
        bar_alpha = 0.18 if is_dim else 0.92
        err_color = SPINE_C if is_dim else TXT

        ax.bar(
            x_centers, means, width,
            yerr=cis if (s >= 1.0 and not is_dim) else None,
            color=color, alpha=bar_alpha,
            edgecolor=BAR_E, linewidth=0.8, label=alias,
            error_kw=dict(elinewidth=1.0, capsize=3, capthick=1.0,
                          ecolor=err_color),
            zorder=2,
        )

        # Accumulate for trend (only visible, non-dim, at full height)
        if key not in hide_keys and not is_dim and s >= 1.0:
            for g in range(G):
                trend_means_per_x[g].append(float(means[g]))

    # Draw trend line across precision if requested
    if draw_trend and metric_key == "precision":
        avg_per_x = [np.mean(vals) if vals else 0.0 for vals in trend_means_per_x]
        ax.plot(idx, avg_per_x, color="#F47C7C", linewidth=3.0, linestyle=":",
                zorder=10, alpha=0.9)

    # Axis styling
    if x_axis_col == "n":
        ax.set_xlabel("n", color=TXT, fontsize=26)
    else:
        ax.set_xlabel(r"$\eta$", color=TXT, fontsize=28)
    ax.set_xticks(idx)
    ax.set_xticklabels([str(int(x)) for x in x_values])
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_edgecolor(SPINE_C); sp.set_linewidth(1.4)
    ax.tick_params(colors=TXT, labelsize=20)
    ax.yaxis.grid(True, color=GRID_C, linestyle=":", alpha=0.5)
    ax.xaxis.grid(False)
    ax.set_ylim(0.0, 1.10)


def render_frame(df_e, df_n, out_path,
                 height_scale=None, dim_keys=None, hide_keys=None,
                 legend_methods=None, draw_trend=False):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=False, sharey=False)
    fig.patch.set_facecolor(BG)

    # Row 1: varying sample size n (fixed η=5)
    for j, (mk, mn) in enumerate(METRICS):
        plot_bars_on_ax(axes[0, j], df_n, "n", N_TICKS, mk,
                        height_scale=height_scale, dim_keys=dim_keys,
                        hide_keys=hide_keys, draw_trend=draw_trend)
        axes[0, j].set_ylabel(mn, color=TXT, fontsize=14)

    # Row 2: varying effect size η (fixed n=500)
    for j, (mk, mn) in enumerate(METRICS):
        plot_bars_on_ax(axes[1, j], df_e, "effect_scale", ETA_TICKS, mk,
                        height_scale=height_scale, dim_keys=dim_keys,
                        hide_keys=hide_keys, draw_trend=draw_trend)
        axes[1, j].set_ylabel(mn, color=TXT, fontsize=14)

    for ax in axes.ravel():
        leg = ax.get_legend()
        if leg: leg.remove()

    # Legend: show only the requested subset
    leg_methods = legend_methods if legend_methods is not None else METHODS
    handles = [Patch(facecolor=m[1], edgecolor=BAR_E, label=m[2]) for m in leg_methods]
    legend = fig.legend(
        handles, [h.get_label() for h in handles],
        loc="lower center", ncols=len(handles), fontsize=13,
        bbox_to_anchor=(0.5, -0.01),
        frameon=True, fancybox=True, framealpha=1.0,
        edgecolor=SPINE_C, facecolor=BG,
        borderpad=0.6, labelspacing=0.8,
        handlelength=2.6, handletextpad=0.6, columnspacing=1.2,
    )
    legend.get_frame().set_linewidth(1.1)
    for text in legend.get_texts():
        text.set_color(TXT)

    plt.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(out_path, format="png", dpi=200, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)


if __name__ == "__main__":
    df_e, df_n = _load_data()

    # Phase 1: baselines grow (NEMS hidden)
    print("Phase 1: baselines grow ...")
    for i in range(N_FRAMES):
        t = ease_out(i / (N_FRAMES - 1))
        hs = {m[0]: t for m in BASELINES}
        render_frame(
            df_e, df_n,
            os.path.join(FRAMES_DIR, f"grow_base_{i:02d}.png"),
            height_scale=hs, hide_keys=NEMS_KEYS,
            legend_methods=BASELINES,
        )

    # Phase 2: trend line on precision (static, baselines at full, NEMS hidden)
    print("Phase 2: trend line ...")
    render_frame(
        df_e, df_n,
        os.path.join(FRAMES_DIR, "trend.png"),
        height_scale={m[0]: 1.0 for m in BASELINES},
        hide_keys=NEMS_KEYS, draw_trend=True,
        legend_methods=BASELINES,
    )

    # Phase 3: baselines dim, NEMS (ours) grows in
    print("Phase 3: NEMS grows ...")
    for i in range(N_FRAMES):
        t = ease_out(i / (N_FRAMES - 1))
        hs = {m[0]: 1.0 for m in BASELINES}
        hs[NEMS_METHOD[0]] = t
        render_frame(
            df_e, df_n,
            os.path.join(FRAMES_DIR, f"add_nems_{i:02d}.png"),
            height_scale=hs, dim_keys=BASELINE_KEYS,
        )

    # Final static
    render_frame(df_e, df_n, os.path.join(HERE, "figure_full.png"))
    print("Done.")
