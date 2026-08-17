"""H1 and H2 estimation.

Ranks within a decision are a permutation, so rows are not independent. Standard
errors are cluster-robust by decision. The naive OLS standard error is computed
too, because the gap between them is how wrong a reader would be who took the
obvious approach.
"""
from __future__ import annotations
import numpy as np


def ols_cluster(X, y, clusters):
    """OLS with a cluster-robust (CR1) sandwich.
        V = (X'X)^-1 [ sum_g X_g' u_g u_g' X_g ] (X'X)^-1
    with finite-sample correction G/(G-1) * (N-1)/(N-K).
    Returns (beta, se_cluster, se_naive)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    clusters = np.asarray(clusters)
    N, K = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    meat = np.zeros((K, K))
    groups = np.unique(clusters)
    for g in groups:
        m = clusters == g
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    G = len(groups)
    corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 else 1.0
    V_cl = corr * (XtX_inv @ meat @ XtX_inv)
    s2 = float(u @ u) / (N - K)
    return beta, np.sqrt(np.diag(V_cl)), np.sqrt(np.diag(s2 * XtX_inv))


def bootstrap_over_decisions(values, n_boot=4000, alpha=0.05, seed=0):
    """Resample DECISIONS, not rows. The unit of independence is the decision."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, float)
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    draws = v[idx].mean(axis=1)
    lo, hi = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return float(v.mean()), float(lo), float(hi)


def vif(X):
    """Variance inflation per column. A significant coefficient with a VIF of 12
    is not a finding, and recency, verbosity and causal rank are correlated by
    construction, so this gets reported."""
    X = np.asarray(X, float)
    out = []
    for j in range(X.shape[1]):
        others = np.delete(X, j, axis=1)
        if others.shape[1] == 0:
            out.append(1.0); continue
        b = np.linalg.pinv(others.T @ others) @ (others.T @ X[:, j])
        resid = X[:, j] - others @ b
        ss_tot = float(((X[:, j] - X[:, j].mean()) ** 2).sum())
        r2 = 1 - float(resid @ resid) / ss_tot if ss_tot > 0 else 0.0
        out.append(1.0 / max(1e-12, 1 - r2))
    return np.array(out)
