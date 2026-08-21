# Paper outline

**Started:** 2026-08-21 · **Status:** structure and argument order. Not drafted.

Gated on [`prior-art.md`](../prior-art.md) §4 — two survey items can still change the contribution,
and drafting before they are done risks writing a claim the literature already owns.

---

## Working title

Not *"Autonomous Economic Governance: A Layer and a Standard."* That title invites the obvious
response — so did Microsoft, and so did OASIS in 2003.

Candidates, ordered by how well the paper could defend them:

1. **"Attributed pre-execution governance for autonomous payments, and a benchmark for it"**
2. "What a spend control can honestly promise: bounded, not eliminated"
3. "Governing irreversible machine payments: a conformance model and an adversarial benchmark"

(1) leads with the two strongest claims and names the artefact. Preferred.

## Contribution statement — three claims, in dependency order

Ordered so each earns the next. The benchmark comes first because it is the artefact that makes the
other two measurable rather than asserted.

1. **A reproducible adversarial benchmark** for pre-execution economic governance, whose scoring
   separates *defended* from *defended by a control the attack does not target*, with sealed
   provenance including a superseded record.
2. **Attribution as a required and independently conformance-scored property**, and the observation
   that requiring it forces a normative evaluation order even where the verdict is
   order-independent.
3. **"Bounded, not eliminated"** as a disclosure obligation: a specification that requires an
   implementation to state the residual its control leaves behind.

**AEGL and AEGS are the vehicle.** The layer is how (2) is delivered; the standard is how (2) and
(3) become checkable by someone else. Neither is the contribution, and presenting them as such is
the version a reviewer rejects.

## Structure

| § | Content | Source |
|---|---|---|
| 1 | **Introduction.** Agents can pay; payment rails do not govern the payer. x402: 75.41M transactions and $24.24M in 30 days — a **$0.32 average** — with no buyer-side authorization specified | x402.org, verified 2026-08-21 |
| 2 | **Why irreversibility changes the controls.** No chargeback, no recall, no issuer. Detective controls buy a description of a loss rather than a recovery, so the control point moves to *before* | `docs/stablecoins.html` |
| 3 | **Related work, conceding the surface.** XACML/OPA/Cedar, macaroons, Certificate Transparency, card controls, Microsoft AGT, transaction monitoring. **This section is why the narrow claim is credible** | [`prior-art.md`](../prior-art.md) |
| 4 | **Definition.** An AEGL renders a deterministic, attributable verdict on a proposed economic action before execution, and emits evidence sufficient to reconstruct which control produced it. **Includes card authorization systems, deliberately** | `PLAN.md` |
| 5 | **Attribution, and the order asymmetry.** The verdict is order-independent; the attribution is not. Dispositive controls. Why this must be *required* and *scored*, not optional | AEGS VERD-4/4a |
| 6 | **The benchmark.** 18 attacks, four outcomes, why `DEFENDED_BY_ACCIDENT` is a finding. Results: 15/1/2/0 | EXP-010 |
| 7 | **Two case studies in bounded-not-eliminated.** Count envelopes: unbounded → bounded by a chosen number. Anchoring: truncation detectable *beyond the last publication*. **Both include the vector that asserts the limit** | EXP-009, EXP-010, EVID-6a |
| 8 | **What the measurements cost.** ~170 µs p50 over ten runs, **range 139–330**, zero tokens. Includes the story of the single-run 128 µs that sat below its own distribution's minimum | EXP-007 |
| 9 | **Limitations.** Own-author benchmark (W6.4); structuring open; anchoring bounded; no independent implementation; one rail; regulatory obligations fall on issuers, not on a library | [`claims-register.md`](../claims-register.md) §3 |
| 10 | **Conclusion and the open question.** The honest one: can a governance standard be validated by anyone other than its author? | — |

## The paper's own discipline

Three rules, each mirroring one the codebase enforces.

1. **Every number cites a sealed record.** No number appears that
   `experiment.py verify` cannot confirm.
2. **Every limitation from a cited record is carried forward.** EXP-007 through EXP-010 each have a
   limitations section; §9 is their union, not a summary.
3. **The corrected measurement is included, not tidied away.** EXP-009 supersedes EXP-008 because a
   measurement was wrong. A record lineage containing a correction is better evidence of method than
   a clean one, and hiding it would be the exact failure the paper claims to guard against.

## Blocked on

- **`prior-art.md` §4, the two highest-risk surveys.** Transparency-log literature could shrink §7's
  anchoring contribution to "applied to a spend journal." ISO 8583 / EMV could already contain §4's
  entire model.
- **A real literature search for existing benchmarks.** §6's claim to be first rests on one pass.
- **P0.1** — the benchmark needs to be a presentable artefact before a paper can cite it as one.

## Deliberately not in this paper

The x402 proposal. Different reader, opposite virtues — see [`../README.md`](../README.md). The
proposal should cite this paper, not contain it, and it should come after the U3 contributions have
earned the standing to be read.
