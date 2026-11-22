"""
Figure 2 — Information curve with the human-usable frontier (Gaussian-IB form).

Message: for a fixed control-layer target Y, any representation Z of the measured
state X_obs trades rate I(X;Z) against relevance I(Z;Y). The achievable curve over
X_obs saturates at the observation ceiling C_obs = I(X_obs;Y); true biological
sufficiency R* lies above it (Delta_obs: never measured). Representations of
human-usable form (a few nameable categories plus a few directly read quantities)
have their own, lower frontier, which saturates at the cognitive ceiling
C_human(Y). The disease label lies BELOW that frontier. Its recoverable deficit
Delta_label = C_obs - I(Z_label;Y) splits into
    Delta_part = C_human(Y) - I(Z_label;Y)   (a better human-usable code would close it)
    Delta_ceil = C_obs - C_human(Y)          (only a machine-read representation can)
Only Delta_ceil supports the thesis. The foundation-model point is drawn hollow
because its position is the hypothesis under test, not a result.

Curve construction: Gaussian-IB form, piecewise-concave with kinks where successive
canonical directions activate (Chechik, Globerson, Tishby & Weiss, JMLR 2005). The
last two directions are treated as unmeasured. The human-usable frontier is a
schematic saturating curve kept below the achievable curve. No units: schematic.

V3 (revision): C_human moved from the rate axis to the relevance axis as a class
ceiling; label drawn below the frontier; Delta_part / Delta_ceil split; FM point
hollow ("predicted"); axis units and tick values removed.
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

# canonical correlations between TRUE patient state X and target Y, decreasing
rho = np.array([0.95, 0.88, 0.78, 0.66, 0.5])
relY = -0.5 * np.log(1 - rho**2)        # relevant info contributed by each direction
eff  = rho**2                           # relevance-per-rate slope of each segment
dR   = relY / eff                       # rate needed to extract relY[i] at slope eff_i
rate_break = np.concatenate([[0], np.cumsum(dR)])
rel_break  = np.concatenate([[0], np.cumsum(relY)])

R_star = rel_break[-1]                  # I(X_true;Y)
N_OBS  = 3                              # directions captured by instruments
C_obs  = rel_break[N_OBS]               # I(X_obs;Y)
rate_obs = rate_break[N_OBS]

# achievable curve over X_obs
xs, ys = [0.0], [0.0]
for i in range(N_OBS):
    xs += list(np.linspace(rate_break[i], rate_break[i + 1], 40))
    ys += list(np.linspace(rel_break[i],  rel_break[i + 1],  40))
xs += list(np.linspace(rate_obs, rate_obs + 1.6, 20))
ys += [C_obs] * 20
xs, ys = np.array(xs), np.array(ys)
dmax = rate_break[N_OBS + 1] + 1.1

def achievable(r):
    return np.interp(r, xs, ys)

# human-usable frontier: saturates at C_human, never above the achievable curve
C_human = rel_break[1] + 0.62 * relY[1]
rh = np.linspace(0, dmax, 400)
a = np.maximum(0.86 * achievable(rh), 1e-9)          # visibly below the achievable curve
human = (a**-6 + C_human**-6) ** (-1 / 6)              # smooth saturation at C_human
C_human = human.max()                                  # ceiling = the frontier's plateau

# operating points
r_label = rate_break[1] * 0.85
y_label = np.interp(r_label, rh, human) - 0.30          # below the human-usable frontier
r_sub   = 1.75
y_sub   = np.interp(r_sub, rh, human) - 0.06            # close to the frontier
r_fm    = rate_obs + 0.35
y_fm    = C_obs                                         # hypothesized position

fig, ax = plt.subplots(figsize=(8.7, 5.8))

# never-measured band and R*
ax.fill_between([0, dmax], C_obs, R_star, color="#7f8c8d", alpha=0.10, zorder=0)
ax.axhline(R_star, ls="--", lw=1.0, color="#555555", zorder=1)
ax.text(dmax, R_star + 0.02, r"$R^{*}$  biological sufficiency (theoretical)",
        fontsize=7.8, color="#555555", ha="right", va="bottom")
ax.axhline(C_obs, ls="--", lw=1.2, color="#2471a3", zorder=2)
ax.text(dmax, C_obs + 0.02, r"$C_{\mathrm{obs}}$  observation ceiling (estimable from below)",
        fontsize=7.8, color="#2471a3", ha="right", va="bottom")

# cognitive ceiling as a relevance level, with a pale band: it varies by setting
ax.axhspan(C_human - 0.07, C_human + 0.07, color="#c0392b", alpha=0.07, lw=0, zorder=0)
ax.axhline(C_human, ls="--", lw=1.2, color="#c0392b", zorder=1)
ax.text(dmax, C_human + 0.09, r"$C_{\mathrm{human}}(Y)$  cognitive ceiling (heuristic; varies by setting)",
        fontsize=7.8, color="#c0392b", ha="right", va="bottom")

# curves
ax.plot(xs, ys, "-", lw=2.3, color="#2c3e50", zorder=3)
ax.text(3.70, C_obs - 0.07, "all representations of the record",
        fontsize=7.6, color="#2c3e50", ha="left", va="top", style="italic")
ax.plot(rh, human, "-", lw=1.8, color="#c0392b", alpha=0.85, zorder=3)
ax.text(3.15, C_human - 0.07, "representations of human-usable form",
        fontsize=7.6, color="#a93226", ha="left", va="top", style="italic")

# points
ax.scatter([r_label], [y_label], s=110, color="#2c7fb8", edgecolor="white", linewidth=1.3, zorder=6)
ax.annotate("Disease label", (r_label, y_label), xytext=(r_label + 0.32, y_label - 0.30),
            fontsize=8.4, color="#2c7fb8", ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.7, color="#2c7fb8"))
ax.scatter([r_sub], [y_sub], s=110, color="#16a085", edgecolor="white", linewidth=1.3, zorder=6)
ax.annotate("Subtypes /\nendotypes", (r_sub, y_sub), xytext=(r_sub + 0.35, y_sub - 0.55),
            fontsize=8.4, color="#16a085", ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.7, color="#16a085"))
ax.scatter([r_fm], [y_fm], s=120, facecolor="white", edgecolor="#e67e22", linewidth=2.0, zorder=6)
ax.annotate("Unrestricted representation,\ne.g. foundation model (predicted)", (r_fm, y_fm),
            xytext=(3.60, 2.02), fontsize=8.4, color="#e67e22", ha="left", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.7, color="#e67e22"))

# stacked deficits at the label's rate
bx = r_label - 0.16
def vbrace(y0, y1, color, label, dx=-0.06):
    ax.add_patch(FancyArrowPatch((bx, y0 + 0.015), (bx, y1 - 0.015), arrowstyle="<->",
                 mutation_scale=10, lw=1.3, color=color, zorder=5))
    ax.text(bx + dx, (y0 + y1) / 2, label, fontsize=8.4, color=color, ha="right", va="center")
vbrace(y_label, C_human, "#2c7fb8", r"$\Delta_{\mathrm{part}}$")
vbrace(C_human, C_obs, "#8e44ad", r"$\Delta_{\mathrm{ceil}}$")
vbrace(C_obs, R_star, "#7f8c8d", r"$\Delta_{\mathrm{obs}}$")
ax.plot([bx, r_label], [y_label, y_label], ls=":", lw=0.8, color="#2c7fb8", zorder=4)

ax.text(2.55, 0.62,
        r"$\Delta_{\mathrm{label}}=\Delta_{\mathrm{part}}+\Delta_{\mathrm{ceil}}$"
        "\n" r"$\Delta_{\mathrm{part}}$: better labels could close it"
        "\n" r"$\Delta_{\mathrm{ceil}}$: only a machine-read representation can"
        "\n" r"$\Delta_{\mathrm{obs}}$: needs better measurement",
        fontsize=7.8, color="#4a235a", ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f5eef8", ec="#8e44ad", lw=0.7))

# in-image note and title removed (2026-11-23): JMIR keeps notes and titles out of figure images; the caption carries them

ax.set_xlim(0, dmax)
ax.set_ylim(0, R_star + 0.45)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel(r"Rate  $I(X;Z)$: information the representation keeps about the patient", fontsize=9)
ax.set_ylabel(r"Relevance  $I(Z;Y)$: information about target $Y$", fontsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

plt.tight_layout()
for ext in ["pdf", "png"]:
    fig.savefig(f"figures/fig2_ib_staircase.{ext}", dpi=300, bbox_inches="tight")
print(f"wrote figures/fig2_ib_staircase.pdf / .png | R*={R_star:.3f} C_obs={C_obs:.3f} C_human={C_human:.3f}")
