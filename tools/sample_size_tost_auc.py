"""
Sample size for the paired AUROC contrasts in Multimedia Appendix 3, section 6.

Two models are scored on the same patients; the AUROC difference has variance
2 * Var(AUC) * (1 - r), with Var(AUC) from Hanley-McNeil and r the correlation between
the two AUROC estimates. The analytic standard deviation is checked by simulation with
binormal scores.

Decision rule being powered (Appendix 3, section 5):
  equivalence  - one-sided: upper 95% confidence bound of the cognitive-ceiling deficit < delta,
                 power 80% when the true difference is 0 (the deficit cannot be negative
                 in the population, so equivalence is judged against the upper bound only);
  superiority  - two-sided test of zero at Holm-adjusted alpha (0.05/3 at the first step
                 for three primary targets), power 80% when the true difference is delta.

Usage: python tools/sample_size_tost_auc.py
"""
import numpy as np
from scipy.stats import norm
from sklearn.metrics import roc_auc_score


def var_auc(A, n, prev):
    n1, n0 = n * prev, n * (1 - prev)
    Q1, Q2 = A / (2 - A), 2 * A * A / (1 + A)
    return (A * (1 - A) + (n1 - 1) * (Q1 - A * A) + (n0 - 1) * (Q2 - A * A)) / (n1 * n0)


def sd_diff(A, n, prev, r):
    return np.sqrt(2 * var_auc(A, n, prev) * (1 - r))


def n_equivalence(A, prev, r, delta, alpha=0.05, power=0.8):
    for n in range(50, 40000, 5):
        if norm.cdf(delta / sd_diff(A, n, prev, r) - norm.ppf(1 - alpha)) >= power:
            return n


def n_superiority(A, prev, r, delta, alpha=0.05 / 3, power=0.8):
    for n in range(50, 40000, 5):
        if norm.cdf(delta / sd_diff(A, n, prev, r) - norm.ppf(1 - alpha / 2)) >= power:
            return n


def simulated_sd(n, A=0.75, prev=0.5, rho_scores=0.8, reps=2000, seed=1):
    rng = np.random.default_rng(seed)
    mu = np.sqrt(2) * norm.ppf(A)
    diffs, pairs = [], []
    for _ in range(reps):
        y = rng.random(n) < prev
        z = rng.standard_normal((n, 2))
        z[:, 1] = rho_scores * z[:, 0] + np.sqrt(1 - rho_scores ** 2) * z[:, 1]
        s = z + mu * y[:, None]
        a1, a2 = roc_auc_score(y, s[:, 0]), roc_auc_score(y, s[:, 1])
        diffs.append(a1 - a2); pairs.append((a1, a2))
    return np.std(diffs), np.corrcoef(np.array(pairs).T)[0, 1]


if __name__ == "__main__":
    print("AUROC 0.75; patients with the outcome assessed in the evaluation (validation) cohort")
    print("prevalence  r    delta  equivalence(one-sided)  superiority(Holm 0.05/3)")
    for prev in (0.5, 0.3):
        for r in (0.7, 0.5):
            for d in (0.05, 0.03):
                print(f"{prev:9.1f}  {r:.1f}  {d:.2f}   {n_equivalence(0.75, prev, r, d):>10}"
                      f"   {n_superiority(0.75, prev, r, d):>12}")
    for n in (300, 500):
        sd, r = simulated_sd(n)
        print(f"simulation n={n}: sd(diff)={sd:.4f}, corr={r:.2f}; analytic sd={sd_diff(0.75, n, 0.5, r):.4f}")
