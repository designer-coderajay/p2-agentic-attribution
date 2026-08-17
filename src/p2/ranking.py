"""Plackett-Luce rank-ordered regression, and the H3 statistic.

The prereg names a rank-ordered model as the primary H2 specification. Only
OLS-on-score was validated until now: for span duration and token count we do
observe a continuous score, but the LLM-judge attributor yields only an ordering,
and OLS on ranks is not a model of the ranking process.

PL is exactly the model where latent_j = x_j' beta + Gumbel(0,1) and the observed
ranking sorts the latents. Log-likelihood for one decision's ranking pi:

    L = sum_t [ theta_{pi(t)} - log sum_{j in R_t} exp(theta_j) ],  theta = X beta

with R_t the set still unranked at position t. Gradient and Hessian are analytic,
so this is Newton, not a black-box optimiser.

Each decision contributes ONE ranking and is one independent observation, so the
sandwich is V = H^-1 (sum_d s_d s_d') H^-1. No design choice about clustering:
the decision IS the unit.
"""
from __future__ import annotations
import numpy as np


def _logsumexp(v):
    m = v.max()
    return m + np.log(np.exp(v - m).sum())


def pl_negloglik_grad_hess(beta, decisions):
    """decisions: list of (X_d, order_d), order_d indexing rows of X_d from most
    to least salient. Returns (nll, gradient, Hessian, per-decision scores)."""
    K = len(beta)
    nll = 0.0
    grad = np.zeros(K)
    H = np.zeros((K, K))
    scores = []
    for X, order in decisions:
        theta = X @ beta
        s_d = np.zeros(K)
        remaining = list(order)
        for t in range(len(order) - 1):
            idx = np.array(remaining)
            th = theta[idx]
            lse = _logsumexp(th)
            p = np.exp(th - lse)
            Xr = X[idx]
            wbar = p @ Xr
            nll -= (theta[remaining[0]] - lse)
            s_d += X[remaining[0]] - wbar
            H += (Xr.T * p) @ Xr - np.outer(wbar, wbar)
            remaining.pop(0)
        grad += s_d
        scores.append(s_d)
    return nll, grad, H, np.array(scores)


def fit_plackett_luce(decisions, K, tol=1e-9, max_iter=60):
    """Newton with step-halving. Returns (beta, se_cluster, n_iter).

    No intercept: PL is invariant to adding a constant to every theta within a
    decision, so an intercept is unidentified. Including one silently produces a
    singular Hessian, so it is excluded by construction rather than caught later."""
    beta = np.zeros(K)
    nll_prev = np.inf
    for it in range(1, max_iter + 1):
        nll, grad, H, _ = pl_negloglik_grad_hess(beta, decisions)
        step = np.linalg.solve(H + 1e-10 * np.eye(K), grad)
        lam = 1.0
        for _ in range(30):
            if pl_negloglik_grad_hess(beta + lam * step, decisions)[0] <= nll:
                break
            lam *= 0.5
        beta = beta + lam * step
        if abs(nll_prev - nll) < tol:
            break
        nll_prev = nll
    _, _, H, scores = pl_negloglik_grad_hess(beta, decisions)
    Hinv = np.linalg.pinv(H)
    G = len(decisions)
    corr = G / (G - 1.0) if G > 1 else 1.0
    V = corr * (Hinv @ (scores.T @ scores) @ Hinv)
    return beta, np.sqrt(np.diag(V)), it


def wilson(k, n, z=1.959963985):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = (z / d) * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    lo, hi = c - h, c + h
    # Exact boundary cases, not a clamp. At k = 0 the Wilson centre and half-width
    # are algebraically equal (both z^2/(2 n d)), so the lower bound is exactly
    # zero; floating-point cancellation leaves ~2e-19. A correct estimate of a
    # zero rate then falls outside its own interval, which is how the H3 closed-
    # form check failed on first run. Every zero cell in the H3 (delta, tau) grid
    # would have been wrong. Symmetrically at k = n.
    if k == 0:
        lo = 0.0
    if k == n:
        hi = 1.0
    return float(min(max(lo, 0.0), 1.0)), float(min(max(hi, 0.0), 1.0))


def h3_statistic(causal_list, obs_rank_list, delta=1.0, tau=0.5):
    """Fraction of decisions with a causally dominant node the trace ranks as
    negligible.

    dominant  : |causal_j| >= delta * max_i |causal_i|
    negligible: obs_rank_j > tau * n   (rank 1 = most salient)

    delta and tau are researcher degrees of freedom. They MUST be pre-registered
    and reported across a grid, exactly as P1 reports the claim map at three
    granularities. A single (delta, tau) pair is a tuned number."""
    hits = 0
    n_dec = len(causal_list)
    for causal, obs_rank in zip(causal_list, obs_rank_list):
        causal = np.abs(np.asarray(causal, float))
        obs_rank = np.asarray(obs_rank, float)
        n = len(causal)
        if np.any((causal >= delta * causal.max()) & (obs_rank > tau * n)):
            hits += 1
    lo, hi = wilson(hits, n_dec)
    return hits / n_dec, lo, hi, hits, n_dec
