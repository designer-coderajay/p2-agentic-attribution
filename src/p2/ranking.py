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


def fit_plackett_luce(decisions, K, tol=1e-9, max_iter=60, ridge=0.0):
    """Newton with a step-halving safeguard.
    Returns (beta, se_cluster, V, n_iter).

    No intercept: PL is invariant to adding a constant to every theta within a
    decision, so an intercept is not identified. Including one would silently
    produce a singular Hessian, so it is excluded by construction.

    Returns the FULL covariance matrix, because the pre-registered primary
    contrast is a JOINT test on two coefficients and needs the off-diagonal.

    `ridge` is an L2 penalty, zero by default. Under quasi-complete separation
    the unpenalised MLE diverges: a covariate that predicts the ranking perfectly
    drives its coefficient to infinity and the Wald statistic becomes meaningless
    while looking overwhelmingly significant. The penalty bounds it. Its value is
    a pre-registered constant, never tuned to a result.
    """
    beta = np.zeros(K)
    nll_prev = np.inf
    for it in range(1, max_iter + 1):
        nll, grad, H, _ = pl_negloglik_grad_hess(beta, decisions)
        if ridge > 0.0:
            nll = nll + 0.5 * ridge * float(beta @ beta)
            grad = grad - ridge * beta
            H = H + ridge * np.eye(K)
        step = np.linalg.solve(H + 1e-10 * np.eye(K), grad)
        lam = 1.0
        for _ in range(30):
            cand = beta + lam * step
            cand_nll = pl_negloglik_grad_hess(cand, decisions)[0]
            if ridge > 0.0:
                cand_nll += 0.5 * ridge * float(cand @ cand)
            if cand_nll <= nll:
                break
            lam *= 0.5
        beta = beta + lam * step
        if abs(nll_prev - nll) < tol:
            break
        nll_prev = nll
    _, _, H, scores = pl_negloglik_grad_hess(beta, decisions)
    if ridge > 0.0:
        H = H + ridge * np.eye(K)
    Hinv = np.linalg.pinv(H)
    G = len(decisions)
    corr = G / (G - 1.0) if G > 1 else 1.0
    V = corr * (Hinv @ (scores.T @ scores) @ Hinv)
    return beta, np.sqrt(np.diag(V)), V, it


def separation_diagnostic(beta, se=None, H=None, ridge=0.0,
                          beta_max=25.0, cond_max=1e10):
    """Detect quasi-complete separation in a Plackett-Luce fit.

    Under separation a covariate predicts the ranking perfectly, the unpenalised
    MLE diverges, and the Wald statistic explodes while the p-value looks
    overwhelming. The first end-to-end dry run produced exactly this: a verbosity
    coefficient of +172 with p = 1e-98, from data where token count was nearly
    deterministic in the ranked score.

    TWO SIGNALS, both structural and both independent of sample size:
      1. |beta| exceeding beta_max. Separation drives a coefficient to infinity.
      2. Hessian condition number exceeding cond_max. Near-singularity in the
         direction of the separating covariate.

    A |z| > 40 rule was tried and REMOVED, because it is wrong. z = |beta|/se
    grows like sqrt(N), so any fixed z cut eventually fires on a strong,
    perfectly well-identified effect. Measured on the reference well-behaved
    Gumbel design where PL recovers its own generative model: z = 19.5 at 100
    decisions, 28.0 at 200, 40.8 at 400, 59.5 at 800, 86.0 at 1600. The rule
    would have flagged a genuine H2 rejection as separation, and would have done
    so MORE readily the stronger the result. z measures strength of evidence,
    not degeneracy.

    Read this on the UNPENALISED fit. It is a detector, not an "is it fixed now"
    check: a ridge penalty bounds the estimate without removing the separation,
    and it inflates H by construction, so the conditioning rule is skipped when
    ridge > 0.

    Returns (separated, reason).
    """
    beta = np.asarray(beta, float)
    if np.max(np.abs(beta)) > beta_max:
        return True, f"|beta|max = {np.max(np.abs(beta)):.1f} exceeds {beta_max}"
    if H is not None and ridge == 0.0:
        c = float(np.linalg.cond(H))
        if c > cond_max:
            return True, f"Hessian condition number {c:.2e} exceeds {cond_max:.0e}"
    return False, ("no separation detected" if ridge == 0.0
                   else f"bounded under ridge={ridge}")

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


# --------------------------------------------------------------------------
# The pre-registered primary contrast
# --------------------------------------------------------------------------

def chi2_sf_df2(x: float) -> float:
    """Survival function of chi-square with 2 degrees of freedom.

    For df = 2 this is exactly exp(-x/2): chi-square with 2 df is an exponential
    with mean 2. Exact, not an approximation, and no scipy dependency. The primary
    contrast is 2-df by construction (recency and verbosity), so this covers it
    precisely. Verified against 400k simulated chi2_2 draws: at x = 5.991 it
    returns 0.05001, the textbook critical value.
    """
    return float(np.exp(-x / 2.0))


def joint_wald(beta, V, idx):
    """Joint Wald test that the coefficients at positions `idx` are all zero.

        W = (R b)' (R V R')^-1 (R b),   W ~ chi2_q under H0

    The PRE-REGISTERED PRIMARY CONTRAST is this test with idx = (recency,
    verbosity), q = 2.

    Joint rather than two marginal tests, deliberately: a single 2-df test carries
    no multiplicity correction, whereas two marginal tests need one and invite a
    reviewer to ask which correction and why.
    """
    beta = np.asarray(beta, float); V = np.asarray(V, float)
    idx = list(idx)
    b = beta[idx]
    W = float(b @ np.linalg.solve(V[np.ix_(idx, idx)], b))
    q = len(idx)
    return W, q, (chi2_sf_df2(W) if q == 2 else float("nan"))


# --------------------------------------------------------------------------
# H4
# --------------------------------------------------------------------------

def h4_statistic(mediated_share_list, obs_rank_list, causal_rank_list):
    """H4: the discrepancy concentrates in nodes whose influence is MEDIATED.

    Per node:  gap = obs_rank - causal_rank  (positive = the trace ranks it as
                                              LESS salient than it causally is)
               mediated_share = |ME| / |TE_crn|

    Statistic: Kendall tau_b between mediated_share and gap, per decision,
    bootstrapped over decisions. H4 predicts a POSITIVE association: the more of a
    node's influence travels through what it caused later steps to do, the more
    the trace under-ranks it.

    This is the mechanistic explanation for H1-H3 rather than a fourth symptom,
    and it is the part hardest for prior work to have done, since prior work has
    no direct-effect arm to form a mediated share from.
    """
    from p2.observability import kendall_tau_b
    taus = []
    for ms, obs_r, cau_r in zip(mediated_share_list, obs_rank_list, causal_rank_list):
        ms = np.asarray(ms, float)
        gap = np.asarray(obs_r, float) - np.asarray(cau_r, float)
        keep = np.isfinite(ms) & np.isfinite(gap)
        if keep.sum() >= 2:
            t = kendall_tau_b(ms[keep], gap[keep])
            if np.isfinite(t):
                taus.append(t)
    return np.array(taus)
