# Claims register

**Started:** 2026-08-21 · Every claim the paper intends to make, the evidence for it, and the
claims that **cannot** be supported.

The rule: **a claim without a sealed record or a named test is not a claim, it is a hope.** This
file exists so the paper cannot quietly acquire a sentence nothing backs. It is the same discipline
the codebase applies to coverage counts, pointed at prose.

**Status key:** `supported` — a sealed experiment or named test backs it. `partial` — evidence
exists but is weaker than the wording. `unsupported` — no evidence; either get some or cut the
sentence. `refuted` — investigated and found false.

---

## 1 · Measurement claims

Every number here must trace to a sealed record in
[`aegs/research/experiments`](https://github.com/tesoro-labs/aegs/tree/main/research), verifiable by
`python research/tools/experiment.py verify`.

| Claim | Evidence | Status |
|---|---|---|
| A governed decision costs ~200 µs and zero tokens | EXP-007: p50 median ~170 µs over ten runs, **range 139–330 µs** | `supported`, **with the spread**. The single-run "128 µs" that circulated sits *below* the observed minimum of ten later runs |
| The layer defends 15 of 18 adversarial cases | EXP-010: 15 defended / 1 by accident / 2 undefended / 0 error | `supported` |
| Paced evasion is closed by a count envelope | EXP-010: `RT-ECON-004` moved `UNDEFENDED` → `DEFENDED`, attributed to `treasury` citing `actions_per_day` | `supported` |
| Structuring remains open | EXP-010: `RT-ECON-001` `UNDEFENDED`, $0.04 across 40 payments, nothing refused | `supported` — and it is *published* as open in four documents |
| Closing paced evasion required no new control type | EXP-010 `change` block: configuration plus two snapshot fields, `newControlType: false`, `newClause: false` | `supported` |
| A rate limit does not bound a total | EXP-009: 97 actions/hour under a 100/hour ceiling ran 200 actions over 2.05 h untouched | `supported` |
| Trust farming is defended by the wrong control | EXP-010: `RT-ECON-003` `DEFENDED_BY_ACCIDENT`, refused by `review-negative-roi`, not `risk` | `supported` |

**One measurement claim was wrong and was corrected by superseding, not editing.** EXP-008
described `RT-ECON-004` as "paced exactly at the rate limit"; it was paced *above* the limit and
stopped before the hourly counter could reach it. EXP-009 supersedes it. **This belongs in the
paper** — a record lineage containing a corrected measurement is stronger evidence of discipline
than a clean one.

---

## 2 · Novelty claims

Each is stated at the strength [`prior-art.md`](prior-art.md) currently supports, not at the
strength originally wanted.

| Claim | Status | Note |
|---|---|---|
| Attribution is a *novel* concept | **`refuted`** | XACML 3.0 can carry a `PolicyIdentifierList`. Twenty years old |
| Attribution as a **required** output, not optional | `partial` | Not found in prior art, but the survey is one pass |
| Attribution as an **independently conformance-scored** property | `partial` — **still the strongest remaining claim, and now with an argument behind it** | ISO 8583 DE 39 exists and card networks deliberately keep it vague to stop risk-rule reverse-engineering. That objection is answered: the reader here is the operator who *wrote* the policy, not a counterparty probing it (`prior-art.md` §3a) |
| Normative evaluation order justified by verdict/attribution asymmetry | `partial` | Combining algorithms fix precedence in XACML; the *justification* appears new |
| A reproducible adversarial benchmark for economic governance | `partial` | Absence of prior benchmarks is asserted from one pass. **Must be a real literature search before publication** |
| `DEFENDED_BY_ACCIDENT` as a scoring category | `partial` | The idea that a coincidental pass is a finding. Nearest neighbour unknown |
| "Bounded, not eliminated" as a disclosure obligation in a specification | `partial` | The concept is ordinary risk management; the *conformance requirement to disclose the residual* is the narrow part |
| External anchoring as a contribution | **`refuted` 2026-08-21** | Certificate Transparency's Signed Tree Head already carries **tree size + root hash** — `(length, head)` — with consistency proofs and witness networks. `EVID-6a` is CT's model applied to a spend journal. What survives: requiring it in a governance standard, and naming the *unavailable* case as its own outcome (`prior-art.md` §3a) |
| Absent-degrades / broken-raises for the control layer's own availability | `partial` | Fail-safe vs fail-secure is decades old |
| AEGL is a new architectural category | **`refuted` by our own definition** | The narrowed definition deliberately includes card authorization systems |

---

## 3 · Claims that cannot be made

Listed so nobody reaches for them under deadline.

| Tempting sentence | Why not |
|---|---|
| "tesoro provides regulatory compliance" / "GENIUS Act compliance" | The obligations fall on **Permitted Payment Stablecoin Issuers**, MiCA's on EMT/ART issuers and CASPs, the Travel Rule's on VASPs. tesoro is a library and none of those |
| "AML screening" | A schema with no engine behind it. No list, no matching, no jurisdiction model |
| "Tamper-proof evidence" | `AEGS-0.1-EVID-6` **forbids** the claim, and the prohibition does not relax now that an anchor exists |
| "Truncation is detected" | Detected *beyond the anchor's last publication*. A vector asserts the gap |
| "Structuring is handled" | It is **bounded**, not refused. A test fails if this is ever rounded up |
| "Independently validated" / "conformance-tested by a third party" | W6.4. Every case and attack was written by the author of the system under test |
| "The standard has multiple implementations" | One, plus a deliberately crude 2/7 stub built to prove the suite accepts a foreign adapter |
| "Production-ready" | `0.x`, stated in the README, the CHANGELOG header and the quickstart |
| "Prevents agent overspending" | It *decides and records*. It holds no funds and moves no money |

---

## 4 · Claims needing work before they are usable

| Claim | What is missing |
|---|---|
| "There is no benchmark for agent economic governance" | A real literature search. One pass is not absence |
| "No standard requires attribution" | OPA/Cedar conformance check and NIST/EU AI Act traceability still open. **ISO 8583 is done**: the field exists, accuracy is not enforced, and vagueness is deliberate. Whether any EMV or scheme rule *requires* DE 39 accuracy is the remaining gap |
| "Agent-initiated stablecoin payments are a new AML surface" | Plausible and unsourced. Needs either a citation or downgrading to a stated hypothesis |
| "The delegation clamp is macaroon attenuation" | Verify Birgisson et al. venue, year and exact framing before citing |
| ~~"Certificate Transparency solves the anchoring problem we solve"~~ | **Done, and it does.** The STH is `(length, head)`; consistency proofs detect omission; witnesses detect split-view. `EVID-6a`'s contribution is now stated as "CT's model, required by a governance spec, with the unavailable case named" |
| "$0.32 average x402 payment validates the micropayment thesis" | Verified from x402.org on 2026-08-21: 75.41M transactions, $24.24M / 30 days. **A single observation on one day** — take a second reading before the paper treats it as a trend |

---

## 5 · The strongest paragraph available today

Written out because it is the test of whether the contribution is real. Every number traces to a
sealed record, and every limitation is in the sentence rather than a footnote.

> We present an economic governance layer that renders a deterministic, attributed verdict on a
> proposed payment before it executes, and an adversarial benchmark of 18 attacks that scores such
> layers. Neither the policy evaluation nor the evidence structure is new — the former is XACML's
> lineage and the latter is Certificate Transparency's, applied to a spend journal. The benchmark's scoring separates *defended* from **defended by a control the attack does
> not target**, which we count as a finding: on our own implementation this distinguishes a genuine
> defence from a coincidence in one of eighteen cases. Two attacks remain undefended and are
> published as such. Closing a third required no new control — only a counting window longer than an
> hour, which the specification had permitted from the first version and no implementation had used;
> we record the measurement that misdescribed the attack, and the superseding record that corrected
> it. Every case and every attack was written by the authors of the system under test, which is the
> principal limitation of this work.

**Note what that paragraph does not claim:** no new category, no compliance, no tamper-proofing, no
independent validation. It is *narrower than the project's own documentation was three days ago*,
and it is the version that survives review.
