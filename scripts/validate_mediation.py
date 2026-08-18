"""Validate the tool mediation layer (WS2.6).

This module is the reason P2 can run against a live regulated system at all.
arXiv 2606.08275 declares real tools with side effects out of scope and
demonstrates on mocked tools. The claim that we remove that exclusion rests
entirely on this file, and until now it had no test.

The property that matters most is a SAFETY property, not a statistical one:

    a tool classified EFFECTFUL_UNSAFE must never execute during a counterfactual
    rollout, under any operator, under any code path, even when a callable is
    supplied.

A penny-drop verification moves money. If that guarantee has a hole, the failure
is not a wrong number in a table, it is a real transaction against a real bank
account. Tested by handing the mediator a live function that records every
invocation, then asserting the recorder stays empty.
"""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from p2.mediation import (Purity, ToolSpec, ToolMediator, MediationError,
                          request_hash)

FAILS = []


def check(name, cond, detail=""):
    print(f"   {'ok  ' if cond else 'FAIL'}  {name}" + (f"   {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


def main():
    print("1. ToolSpec refuses to construct a non-PURE tool without a declared")
    print("   counterfactual environment. Guessing must be impossible, not discouraged.")
    for pur in [Purity.READ_ONLY_VOLATILE, Purity.EFFECTFUL_IDEMPOTENT,
                Purity.EFFECTFUL_UNSAFE]:
        try:
            ToolSpec(name="x", purity=pur)
            check(f"{pur.value} rejected without env", False)
        except ValueError:
            check(f"{pur.value} rejected without env", True)
    try:
        ToolSpec(name="scorecard", purity=Purity.PURE)
        check("PURE allowed without env", True)
    except ValueError:
        check("PURE allowed without env", False)

    print("\n2. THE SAFETY PROPERTY: an EFFECTFUL_UNSAFE tool never executes.")
    executed = []

    def live(payload):
        executed.append(payload)          # a real penny-drop would move money here
        return {"moved": True}

    specs = {
        "penny_drop": ToolSpec("penny_drop", Purity.EFFECTFUL_UNSAFE,
                               counterfactual_env=lambda p, u: {"verified": u < 0.9}),
        "bureau": ToolSpec("bureau", Purity.READ_ONLY_VOLATILE,
                           counterfactual_env=lambda p, u: {"score": 600 + int(u * 200)}),
        "set_flag": ToolSpec("set_flag", Purity.EFFECTFUL_IDEMPOTENT,
                             counterfactual_env=lambda p, u: {"flag": True}),
        "scorecard": ToolSpec("scorecard", Purity.PURE),
    }
    med = ToolMediator(specs=specs)
    med.record_factual("penny_drop", {"acct": "A1"}, {"verified": True})

    r = med.call("penny_drop", {"acct": "A1"}, 0.5, live_fn=live)
    check("identical unsafe request served from cache", r == {"verified": True} and not executed)

    r = med.call("penny_drop", {"acct": "A2"}, 0.5, live_fn=live)
    check("diverged unsafe request refuses to execute", not executed, f"executed={executed}")
    check("diverged unsafe request served from declared env", r == {"verified": True})
    check("refusal is logged, not silent", med.log[-1].refused is True)

    med2 = ToolMediator(specs=specs, allow_sandbox=True)
    med2.call("penny_drop", {"acct": "A3"}, 0.5, live_fn=live)
    check("unsafe still refuses even with allow_sandbox=True", not executed,
          f"executed={executed}")

    print("\n3. Every other purity class routes as specified")
    med3 = ToolMediator(specs=specs)
    med3.record_factual("bureau", {"pan": "P1"}, {"score": 720})
    check("identical volatile request from cache",
          med3.call("bureau", {"pan": "P1"}, 0.5) == {"score": 720})
    out = med3.call("bureau", {"pan": "P2"}, 0.5)
    check("diverged volatile request uses declared env, never a live re-call",
          out == {"score": 700} and med3.log[-1].served_from == "counterfactual_env", f"{out}")

    calls = []
    med3.call("scorecard", {"x": 1}, 0.5, live_fn=lambda p: calls.append(p) or {"s": 1})
    check("PURE re-calls live", len(calls) == 1 and med3.log[-1].served_from == "live_call")

    med4 = ToolMediator(specs=specs, allow_sandbox=False)
    med4.call("set_flag", {"id": 1}, 0.5, live_fn=live)
    check("idempotent uses env when sandbox disabled",
          med4.log[-1].served_from == "counterfactual_env" and not executed)
    med5 = ToolMediator(specs=specs, allow_sandbox=True)
    sb = []
    med5.call("set_flag", {"id": 1}, 0.5, live_fn=lambda p: sb.append(p) or {})
    check("idempotent sandboxes when enabled",
          len(sb) == 1 and med5.log[-1].served_from == "sandbox")

    try:
        med5.call("undeclared_tool", {}, 0.5)
        check("undeclared tool raises", False)
    except MediationError:
        check("undeclared tool raises", True)

    print("\n4. request_hash is content-addressed and order-independent")
    a = request_hash("t", {"x": 1, "y": 2})
    b = request_hash("t", {"y": 2, "x": 1})
    c = request_hash("t", {"x": 1, "y": 3})
    d = request_hash("u", {"x": 1, "y": 2})
    check("key order does not change the hash", a == b)
    check("different payload changes the hash", a != c)
    check("different tool changes the hash", a != d)
    check("hash is stable across calls", a == request_hash("t", {"x": 1, "y": 2}))

    print("\n5. summary() reports the rates the paper needs")
    s = med.summary()
    check("call count", s["calls"] == len(med.log), f"{s}")
    check("rates in [0,1]", all(0.0 <= s[k] <= 1.0 for k in
          ["factual_cache_rate", "counterfactual_env_rate", "unsafe_refusal_rate"]))
    check("empty mediator reports zero calls", ToolMediator(specs=specs).summary() == {"calls": 0})

    print()
    if FAILS:
        print("FAILURES:", FAILS)
        sys.exit(1)
    print("All mediation checks passed.")
    print("No EFFECTFUL_UNSAFE tool executed on any path, including when a live")
    print("callable was supplied and sandboxing was enabled.")
    env = {"python": platform.python_version(), "module": "mediation"}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"env": env, "unsafe_executions": 0},
              open("results/validation_mediation.json", "w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_mediation.json")


if __name__ == "__main__":
    main()
