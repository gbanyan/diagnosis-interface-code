"""
Figure S1 (Multimedia Appendix 1) — The dominant unit of medical
representation across history, limited by measurement and then by usability.

Message: the representation used for clinical reasoning is limited by whichever is
smaller, what could be measured (grey envelope, ~C_obs) or what a human-usable
representation can carry (C_human, red). In early eras measurement is the binding
limit and the used representation tracks it. From roughly the molecular era,
measurement exceeds C_human and the used representation stays just below the
ceiling; the shaded deficit appears only there. Single-purpose machine scores
(e.g. the 21-gene recurrence score) already sit above C_human for one target each.
A foundation-model representation is predicted to reach the measurable envelope for
many targets; it cannot exceed it.

V3 (revision): y-axis is decision-relevant information (schematic), not rate; R*
removed; deficit band restricted to where measurement exceeds C_human; FM point
capped at the envelope and drawn hollow ("predicted"); "first" claim removed;
single-purpose machine-score precedent added; overlapping labels moved.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.linewidth": 0.8,
    "svg.fonttype": "none",
})

stages = ["Symptom", "Disease\nentity", "Pathology", "Molecular", "Precision", "Foundation\nmodel"]
units  = ["symptom /\nsyndrome", "discrete\ndisease entity", "lesion /\ntissue / cell",
          "molecule /\ngene", "subtype /\nendotype", "continuous\nlatent state"]
tech   = ["bedside\nobservation", "nosology /\nthe clinic", "microscope /\nautopsy",
          "biochemistry /\ncrystallography", "omics /\nsequencing", "self-supervised\nlearning / compute"]
eras   = ["17C–", "18–19C", "1761–1858", "1949–2000s", "2003–", "2018–"]

x = np.arange(1, 7)
y_meas = np.array([1.2, 2.1, 3.4, 5.7, 7.4, 9.0])     # measurable (~ C_obs of the era's record)
C_human = 5.0
y_used = np.array([1.0, 1.85, 3.05, 4.55, 4.75])       # stages 1-5: <= min(measurable, C_human)
y_fm = 8.75                                            # predicted; capped below the envelope

fig, ax = plt.subplots(figsize=(9.2, 5.6))

# cognitive ceiling with a pale band: heuristic and setting-dependent
ax.axhspan(C_human - 0.25, C_human + 0.25, color="#c0392b", alpha=0.07, lw=0, zorder=0)
ax.axhline(C_human, ls="--", lw=1.2, color="#c0392b", zorder=1)
ax.text(6.55, C_human + 0.32, r"$C_{\mathrm{human}}$  cognitive ceiling" "\n(heuristic; varies by setting)",
        fontsize=7.6, color="#c0392b", va="bottom", ha="left")

# deficit band only where measurement exceeds the ceiling
xf = np.linspace(1, 6, 400)
mf = np.interp(xf, x, y_meas)
ax.fill_between(xf, C_human, mf, where=mf > C_human, color="#c0392b", alpha=0.08,
                interpolate=True, zorder=0)
ax.annotate("measured, but beyond what a\nhuman-usable representation\ncan carry", xy=(4.55, 5.35),
            xytext=(2.45, 6.4), ha="center", va="center", fontsize=7.6, color="#a93226",
            style="italic", arrowprops=dict(arrowstyle="-", lw=0.7, color="#a93226"))

# measurable envelope
ax.plot(x, y_meas, "-", lw=1.1, color="#7f8c8d", alpha=0.7, zorder=2)
ax.scatter(x, y_meas, s=14, color="#7f8c8d", alpha=0.7, zorder=3)
ax.text(6.55, y_meas[-1], "measurable\n(what the record\ncan contain)", fontsize=7.6,
        color="#7f8c8d", va="center", ha="left")

# representation used for reasoning
ax.plot(x[:5], y_used, "-", lw=2.2, color="#2c7fb8", zorder=4)
ax.scatter(x[:5], y_used, s=90, color="#2c7fb8", edgecolor="white", linewidth=1.2, zorder=5)
ax.plot([x[4], x[5]], [y_used[4], y_fm], ls=(0, (3, 2)), lw=1.8, color="#e67e22", zorder=4)
ax.scatter([x[5]], [y_fm], s=95, facecolor="white", edgecolor="#e67e22", linewidth=2.0, zorder=5)
ax.text(5.92, y_fm + 0.12, "predicted", fontsize=7.4, color="#e67e22", ha="right",
        va="bottom", style="italic")

# precedent: single-purpose machine scores
ax.scatter([5.0], [6.0], s=55, marker="D", facecolor="white", edgecolor="#8e44ad",
           linewidth=1.4, zorder=5)
ax.annotate("single-purpose machine scores\n(e.g. recurrence score), one target each",
            xy=(5.0, 6.0), xytext=(3.45, 8.35), fontsize=7.2, color="#8e44ad",
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.7, color="#8e44ad"))

# representational-unit labels
for xi, yi, u in zip(x[:5], y_used, units[:5]):
    ax.text(xi, yi - 0.38, u, ha="center", va="top", fontsize=7.4, color="#2c7fb8")
ax.text(x[5] - 0.32, y_fm - 0.30, units[5], ha="right", va="top", fontsize=7.4, color="#e67e22")

# which limit binds
ax.annotate("", xy=(0.75, -0.55), xytext=(3.55, -0.55),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color="#5d6d7e"))
ax.text(2.15, -0.42, "limited by measurement", ha="center", va="bottom", fontsize=7.4,
        color="#5d6d7e", style="italic")
ax.annotate("", xy=(3.65, -0.55), xytext=(5.4, -0.55),
            arrowprops=dict(arrowstyle="<->", lw=0.8, color="#5d6d7e"))
ax.text(4.52, -0.42, "limited by usability", ha="center", va="bottom", fontsize=7.4,
        color="#5d6d7e", style="italic")

# enabling technology + era below axis
for xi, t, e in zip(x, tech, eras):
    ax.text(xi, -1.85, t, ha="center", va="top", fontsize=7.0, color="#34495e")
    ax.text(xi, -3.15, e, ha="center", va="top", fontsize=6.8, color="#95a5a6", style="italic")
ax.text(0.30, -1.85, "enabling\ntechnology", ha="left", va="top", fontsize=6.8,
        color="#34495e", fontweight="bold")

ax.set_xlim(0.3, 7.6)
ax.set_ylim(-3.6, 10.0)
ax.set_xticks(x)
ax.set_xticklabels(stages, fontsize=8.8)
ax.tick_params(axis="x", length=0, pad=6)
ax.set_yticks([])
ax.set_ylabel("Decision-relevant information carried (schematic)", fontsize=9)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_position(("data", -0.8))

ax.set_title("The dominant unit of medical representation, limited first by measurement and then by usability",
             fontsize=10.2, pad=12, loc="left", fontweight="bold")

plt.tight_layout()
for ext in ["pdf", "png"]:
    fig.savefig(f"figures/fig1_historical_arc.{ext}", dpi=300, bbox_inches="tight")
print("wrote figures/fig1_historical_arc.pdf / .png")
