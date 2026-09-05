"""Figures for the P2 manuscript.

Design constraints, in the order the dataviz procedure imposes them.

FORM. Figure 1's job is a comparison whose POINT is a failure to separate, so the
two estimands are drawn as small multiples rather than grouped bars: the reader
should see two inert steps matching two live ones in the left panel and vanishing
in the right, without having to trace a legend. Figure 2's job is change over a
continuous quantity with three series, which is a line chart; the empirical points
are overlaid as markers on their closed forms so agreement is visible rather than
asserted.

COLOR LAST, AND BARELY. These are print figures for a greyscale-safe manuscript,
so identity is carried by linestyle, marker and hatch, and colour is only a
secondary cue. That is the print case the skill reserves texture for. Legibility
in greyscale is computed at the foot of this file, not eyeballed.

NO DUAL AXES anywhere. Recessive spines and grid. Serif type to match the
document body.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    # Type 42 (TrueType), NOT matplotlib's default Type 3. Type 3 fonts are a
    # standing rejection reason at several venues, do not scale cleanly, and are
    # not text-searchable. The manuscript body is Type 1 Latin Modern; figures
    # emitting Type 3 would have been the only non-conforming part of the
    # submission, and the byte-level check that first flagged this was wrong in
    # the opposite direction, reporting no embedded fonts at all.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    # Computer Modern, so figure type matches the Latin Modern body text rather
    # than sitting beside it in a different face.
    "font.family": "serif",
    "font.serif": ["cmr10", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.8,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
    "figure.dpi": 200,
})

INK   = "#1A1A1A"
MID   = "#6E6E6E"
LIGHT = "#949494"   # darkened from #B0B0B0: too faint on paper

# ---------------------------------------------------------------- figure 1
# Analytic values, docs/DERIVATIONS.md Part I section 7. q = 0.9, w = 0.5.
steps  = ["0\ninert", "1\nretrieval", "2\ninert", "3\nexecuting"]
te_marg = [-0.50, -0.50, -0.05, -0.05]
te_crn  = [ 0.00, -0.50,  0.00, -0.05]
inert   = [True, False, True, False]

fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.6), sharey=True)
for ax, vals, title in zip(
        axes, [te_marg, te_crn],
        [r"marginal  $\mathrm{TE}_{\mathrm{marg}}$",
         r"common random numbers  $\mathrm{TE}_{\mathrm{crn}}$"], strict=True):
    y = np.arange(len(steps))
    for i, v in enumerate(vals):
        ax.barh(y[i], v, height=0.55,
                color="white" if inert[i] else MID,
                edgecolor=INK, linewidth=0.9,
                hatch="////" if inert[i] else None, zorder=3)
        # Values sit in a column to the RIGHT of zero. The first draft put them
        # at the bar ends, where they collided with the annotation that carries
        # the argument. Bars run left, numbers run right, nothing overlaps.
        if v != 0:
            ax.text(0.035, y[i], f"{v:.2f}", va="center", ha="left",
                    fontsize=8, color=INK, zorder=4)
        else:
            ax.text(0.035, y[i], "0 (exact)", va="center", ha="left",
                    fontsize=8, color=INK, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels(steps)
    ax.invert_yaxis()
    ax.set_xlim(-0.68, 0.30)
    ax.axvline(0, color=INK, linewidth=0.8, zorder=2)
    ax.set_xlabel("effect on the decision")
    ax.set_title(title, pad=6)
    ax.xaxis.grid(True, zorder=0); ax.set_axisbelow(True)
    ax.set_xticks([-0.6, -0.4, -0.2, 0.0])

# The one thing this figure exists to show, marked only on the panel where it
# is true: two pairs of bars are the same length, and one of each pair is inert.
for xpos, rows, _lab in [(-0.50, (0, 1), None), (-0.05, (2, 3), None)]:
    off = xpos - 0.035
    axes[0].plot([off, off], [rows[0] - 0.28, rows[1] + 0.28],
                 color=INK, lw=0.9, zorder=6)
    for r in rows:
        axes[0].plot([off, xpos], [r, r], color=INK, lw=0.9, zorder=6)
axes[0].text(-0.60, 0.5, "identical", rotation=90, va="center", ha="center",
             fontsize=7, color=INK)
axes[0].text(-0.15, 2.5, "identical", rotation=90, va="center", ha="center",
             fontsize=7, color=INK)

from matplotlib.patches import Patch
fig.legend(handles=[
    Patch(facecolor=MID, edgecolor=INK, label="has a path to the outcome"),
    Patch(facecolor="white", edgecolor=INK, hatch="////", label="causally inert")],
    loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.10),
    handlelength=1.6)

fig.tight_layout()
fig.savefig("figures/fig1_two_total_effects.pdf", bbox_inches="tight")
fig.savefig("figures/fig1_two_total_effects.png", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- figure 2
# docs/DERIVATIONS.md Part II section 12. Vocabulary 32, 40,000 draws per point.
tv        = np.array([0.0000, 0.0856, 0.1788, 0.3969, 0.4245, 0.9369])
quant_cf  = np.array([1.0000, 0.7851, 0.4121, 0.2777, 0.3057, 0.0167])
quant_emp = np.array([1.0000, 0.7839, 0.4087, 0.2740, 0.3054, 0.0177])
max_emp   = np.array([1.0000, 0.9142, 0.8221, 0.6075, 0.5801, 0.0654])
sorted_emp= np.array([1.0000, 0.5298, 0.0858, 0.0447, 0.0446, 0.0252])

fig, ax = plt.subplots(figsize=(4.6, 3.1))
grid = np.linspace(0, 1, 200)
ax.plot(grid, 1 - grid, color=INK, lw=1.6, ls="-", zorder=3,
        label=r"maximal coupling, $1-\mathrm{TV}$")
ax.plot(tv, max_emp, ls="none", marker="o", ms=5.5, mfc="white",
        mec=INK, mew=1.2, zorder=5)
ax.plot(tv, quant_cf, color=MID, lw=1.4, ls="--", zorder=3,
        label="shared-$u$ quantile coupling")
ax.plot(tv, quant_emp, ls="none", marker="s", ms=5, mfc="white",
        mec=MID, mew=1.2, zorder=5)
ax.plot(tv, sorted_emp, color=LIGHT, lw=1.4, ls=":", zorder=3,
        label="probability-sorted sampler")
ax.plot(tv, sorted_emp, ls="none", marker="^", ms=5, mfc="white",
        mec=LIGHT, mew=1.2, zorder=5)

# the factor of nine, the single point the figure exists to make
ax.annotate("", xy=(0.1788, 0.8221), xytext=(0.1788, 0.0858),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9), zorder=6)
# NO IN-PLOT TEXT ANNOTATION. Three placements were tried and each collided
# with a series or the legend: beside the arrow it crossed the maximal line,
# beside the legend it crossed the legend, and with a leader it crossed the
# quantile series. The plot is too dense to carry the sentence. The double-headed
# arrow stays and the caption explains it, which is where a paper puts this
# anyway.
ax.set_xlabel(r"total variation distance $\mathrm{TV}(p,q)$")
ax.set_ylabel("probability the branches agree")
ax.set_xlim(-0.02, 1.0); ax.set_ylim(-0.02, 1.05)
ax.grid(True, zorder=0); ax.set_axisbelow(True)
ax.legend(loc="upper right", frameon=False)
fig.tight_layout()
fig.savefig("figures/fig2_coupling_gap.pdf", bbox_inches="tight")
fig.savefig("figures/fig2_coupling_gap.png", bbox_inches="tight")
plt.close(fig)
print("rendered both figures")

# ------------------------------------------------- greyscale check, computed
def luma(hexstr):
    r, g, b = (int(hexstr[i:i+2], 16) / 255 for i in (1, 3, 5))
    lin = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in (r, g, b)]
    return .2126*lin[0] + .7152*lin[1] + .0722*lin[2]

print("\ngreyscale separation of the three series inks (relative luminance):")
inks = {"INK": INK, "MID": MID, "LIGHT": LIGHT}
for a in inks:
    for b in inks:
        if a < b:
            d = abs(luma(inks[a]) - luma(inks[b]))
            print(f"  {a:5} vs {b:5}  delta L = {d:.3f}  {'OK' if d >= 0.10 else 'TOO CLOSE'}")
print("\nseries ink against the paper (white), which the first pass did not check:")
for k, v in inks.items():
    d = abs(luma("#FFFFFF") - luma(v))
    print(f"  {k:5} vs paper   delta L = {d:.3f}  {'OK' if d >= 0.40 else 'TOO FAINT'}")
print("\n  every series also carries a distinct linestyle and marker, so identity")
print("  never depends on tone alone. That is the requirement for print.")
