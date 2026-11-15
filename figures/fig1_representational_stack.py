"""
Figure 1 (headline) — The representational stack: current vs foundation-model medicine.

Left: the disease label is the spine the whole stack is built on (reasoning, trials,
guidelines all defined in its terms). Right: a continuous latent representation is the
substrate of reasoning, and the human-facing layers — diagnosis, evidence/trials,
guidelines — all become communication interfaces read out from it. Diagnosis is one
layer; the thesis (substrate vs interface, generalized up the stack) in one image.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9, "svg.fonttype": "none",
})
BLUE, TEAL, ORANGE, RED, GREY, MUTE = "#2c7fb8", "#16a085", "#e67e22", "#c0392b", "#7f8c8d", "#aab7c4"

def box(ax, cx, cy, w, h, text, fc, ec, tc="#1a1a1a", fs=9, lw=1.3, weight="normal", ls="solid"):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                 boxstyle="round,pad=0.012,rounding_size=0.018", fc=fc, ec=ec, lw=lw, ls=ls, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc, zorder=4, fontweight=weight)

def varrow(ax, cx, y0, y1, color=GREY, lw=1.6):
    ax.add_patch(FancyArrowPatch((cx, y0), (cx, y1), arrowstyle="-|>", mutation_scale=13, lw=lw, color=color, zorder=2))

fig, ax = plt.subplots(figsize=(11.2, 6.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
# panel labels (multi-panel: a = current medicine, b = foundation-model medicine)
ax.text(0.045, 0.975, "a", ha="left", va="center", fontsize=14, fontweight="bold")
ax.text(0.37, 0.975, "b", ha="left", va="center", fontsize=14, fontweight="bold")
W, H = 0.235, 0.092
ys = [0.84, 0.665, 0.49, 0.315, 0.14]

# ---------------- LEFT: current medicine ----------------
LX = 0.185
ax.text(LX, 0.965, "Current medicine", ha="center", fontsize=12, fontweight="bold")
ax.text(LX, 0.922, "every layer built on the disease label", ha="center", fontsize=8.0, color=RED, style="italic")
box(ax, LX, ys[0], W, H, "Observation\n(signs · labs · imaging · omics)", "#f4f6f7", GREY, fs=8.0)
box(ax, LX, ys[1], W, H, "Disease label", "#fdecea", RED, tc=RED, fs=10.5, lw=2.0, weight="bold")
box(ax, LX, ys[2], W, H, "Reasoning", "#f4f6f7", GREY)
box(ax, LX, ys[3], W, H, "Trials · Guidelines · Evidence", "#f4f6f7", GREY, fs=8.4)
box(ax, LX, ys[4], W, H, "Clinical decision", "#f4f6f7", GREY)
for a, b in zip(ys[:-1], ys[1:]):
    varrow(ax, LX, a - H/2, b + H/2, color=RED if b in (ys[1], ys[2]) else GREY)

# ---------------- RIGHT: foundation-model medicine ----------------
RX = 0.55
ax.text(RX, 0.965, "Foundation-model medicine", ha="center", fontsize=12, fontweight="bold")
ax.text(RX, 0.922, "human-facing layers become read-outs from the latent", ha="center", fontsize=8.0,
        color="#0e7c66", style="italic")
box(ax, RX, ys[0], W, H, "Observation\n(signs · labs · imaging · omics)", "#f4f6f7", GREY, fs=8.0)
box(ax, RX, ys[1], W, H, "Latent patient\nrepresentation", "#eafaf6", TEAL, tc="#0e7c66", fs=9.4, lw=2.0, weight="bold")
box(ax, RX, ys[2], W, H, "Reasoning", "#f4f6f7", GREY)
box(ax, RX, ys[4], W, H, "Clinical decision", "#f4f6f7", GREY)
varrow(ax, RX, ys[0] - H/2, ys[1] + H/2, color=TEAL)
varrow(ax, RX, ys[1] - H/2, ys[2] + H/2, color=TEAL)
varrow(ax, RX, ys[2] - H/2, ys[4] + H/2, color=GREY)

# three interface read-outs to the right
IX, IW, IH = 0.86, 0.205, 0.072
iy = [0.715, 0.605, 0.495]
ax.text(IX, 0.80, "external · communication interfaces", ha="center", fontsize=7.8, color="#a85b13", style="italic")
for yy, lab, established in zip(iy, ["Diagnosis", "Evidence / trials", "Guidelines"], [True, False, False]):
    if established:
        box(ax, IX, yy, IW, IH, lab, "#fdf2e9", ORANGE, tc="#a85b13", fs=8.6, lw=1.6, weight="bold")
    else:
        box(ax, IX, yy, IW, IH, lab, "#ffffff", "#d8a679", tc="#b98a5e", fs=8.4, lw=1.1,
            weight="normal", ls=(0, (3, 2)))
# note demoting the two speculative interfaces to an open question
ax.text(IX - IW/2 - 0.015, (iy[1] + iy[2]) / 2, "a further question\nthis paper raises\nbut does not settle",
        ha="right", va="center", fontsize=6.3, color="#b98a5e", style="italic")
# one dashed arrow from reasoning/latent out to the established diagnosis interface
ax.add_patch(FancyArrowPatch((RX + W/2, ys[2] + 0.02), (IX - IW/2 - 0.01, iy[0]),
             arrowstyle="-|>", mutation_scale=12, lw=1.6, color=ORANGE, ls=(0, (4, 2)), zorder=2))
ax.text((RX + W/2 + IX - IW/2)/2, (ys[2] + iy[0])/2 + 0.055, "projected\nout", ha="center", va="center",
        fontsize=7.0, color="#a85b13", style="italic")
# interfaces feed humans
varrow(ax, IX, iy[2] - IH/2, ys[4] + 0.052, color=ORANGE, lw=1.3)
box(ax, IX, ys[4] - 0.002, IW, 0.082, "clinicians · payers ·\nregistries", "#ffffff", MUTE, fs=7.8)

# divider + footing
ax.plot([0.345, 0.345], [0.05, 0.90], ls=(0, (2, 3)), lw=0.9, color="#cfd6dc", zorder=1)
ax.text(0.5, 0.032,
        "The thesis in one image: today the whole stack — reasoning, trials, guidelines — is built on the disease label (left).\n"
        "With foundation models it can run on a latent substrate, and diagnosis becomes a read-out interface (right); whether evidence and guidelines\n"
        "follow is a further question raised, not settled here. The representation medicine reasons over (internal) separates from the one it communicates in (external).",
        ha="center", va="center", fontsize=8.0, color="#34495e", style="italic")

plt.tight_layout()
for ext in ["pdf", "png"]:
    fig.savefig(f"figures/fig1_representational_stack.{ext}", dpi=300, bbox_inches="tight")
print("wrote figures/fig1_representational_stack.pdf / .png")
