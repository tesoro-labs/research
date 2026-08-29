# Paper outline

**Started:** 2026-08-21 · **Contribution revised:** 2026-08-28 · **Status: §1–§7 of 10 drafted** in
[`draft.md`](draft.md), 2026-08-28. §8–§10 outstanding.

The gate held and it earned its keep. *"Drafting before they are done risks writing a claim the
literature already owns"* — three of them did. OAP, PCAS and PayBench are all 2026, all in this
space, and the survey that found them changed the title, the lead claim, and what §3 has to concede.
Full working in [`../prior-art.md`](../prior-art.md) §3b.

---

## Working title

Not *"Autonomous Economic Governance: A Layer and a Standard."* That title invites the obvious
response — so did Microsoft, and so did OASIS in 2003.

**Revised 2026-08-28.** The earlier preference named the benchmark in the title. After the survey
that is the weakest claim, not the strongest, and a title promising a benchmark next to OAP's
4,437-decision CTF invites exactly the comparison this project loses.

Candidates, ordered by how well the paper could defend them:

1. **"Which control decided? Required attribution in pre-execution payment governance"** — after
   §3c, *delegation* cannot appear in the title of a paper that no longer claims it
2. "What a spend control can honestly promise: bounded, not eliminated"
3. "Attributed pre-execution governance for autonomous payments" — accurate, and generic enough
   next to three 2026 systems saying similar things

(1) leads with the question the paper actually answers and names both surviving claims. Preferred.

<details>
<summary>Superseded 2026-08-21 preference</summary>

*"Attributed pre-execution governance for autonomous payments, and a benchmark for it"* — chosen
because it "leads with the two strongest claims and names the artefact." The artefact is no longer
one of the two strongest.

</details>

## Contribution statement — revised 2026-08-28, after the benchmark survey

**The previous three claims did not survive [`prior-art.md` §3b](../prior-art.md) intact, and the
revision is the point of having written them down first.** OAP (arXiv:2603.20953, March 2026) is a
deterministic pre-action authorization system with signed decision records, per-denial reason codes
and a live CTF carrying 4,437 adversarial decisions from external attackers. PCAS is a Datalog
reference monitor doing the same job. PayBench is an adversarial payment-agent benchmark. All 2026.

Two consequences to absorb before writing a word of prose:

1. **The category is not ours.** OAP says PCAS and it *"independently converge on the need for
   deterministic pre-action enforcement as a distinct architectural layer … the category is real,
   not an artifact of a single system's design."* A paper introducing the category would be
   introducing something with three implementations. **The posture is corroboration, not priority**,
   and saying so early is what buys the reader's attention for what follows.
2. **The benchmark is not the lead.** It is smaller than OAP's, its attacks were written by the
   author of the system under test, and — found by reading PayBench — it has **no benign twins**, so
   an implementation that refused everything would score 18/18. That is a defect in the instrument
   and it goes in §9 rather than being discovered by a reviewer.

### The claims, in dependency order

1. **Attribution beyond a denial reason code.** Every surveyed system that attributes at all
   attributes a *refusal*. This one requires the record to name the control that **permitted** an
   action too, defines **precedence when several controls would refuse** (dispositive controls,
   narrowing lattice), and makes the presence of that attribution **independently
   conformance-scorable** by a third party holding only machine-readable vectors. The order
   asymmetry follows and nothing surveyed states it: **the verdict is order-independent, the
   attribution is not**, so requiring attribution forces a normative evaluation order.

2. ~~**A delegation clamp, specified and implemented.**~~ **Withdrawn the same day it was added —
   see [`prior-art.md` §3c](../prior-art.md).** Narrowing-only delegated authority is a 1996
   Internet standard with a chain-reduction algorithm (SPKI/SDSI), a 2014 credential scheme
   (macaroons), a named design pattern (attenuating proxies, membranes), and a 2026 paper with a
   **mechanised Coq proof** that capabilities only narrow under composition (arXiv:2605.24036).
   OAP not having formalised it says something about OAP and nothing about the field.

   What survives — *the record names which step of the chain limited this action* — is an
   **attribution** claim, and it is folded into claim 1 above rather than counted twice.

3. **"Bounded, not eliminated" as a disclosure obligation.** Untouched by every survey so far: a
   specification that requires an implementation to state the *residual* its control leaves behind.
   Count envelopes convert unbounded into bounded-by-a-chosen-number and do not eliminate
   structuring; anchoring makes truncation detectable only *beyond the last publication*. Both ship
   with a vector that asserts the limit.

3b. **`DEFENDED_BY_ACCIDENT` as a scoring rule.** Counting *refused by a control the attack does not
   target* as a finding rather than a pass. OAP records a deny code and never asks whether it was
   the code aiming at the attack; PayBench scores whether a refusal was appropriate, not where it
   came from. **A paragraph in §6, not a section, and not the paper's lead.**

**AEGL and AEGS remain the vehicle, not the contribution.** That was right before the survey and is
more obviously right after it.

### Size, stated plainly

**Three claims, each a paragraph rather than a section.** Attribution (required, scored, on permit
as well as denial, with precedence and the limiting delegation step named); *bounded, not
eliminated* as a disclosure obligation; and one scoring rule. Three surveys removed one claim each,
including one this document invented and refuted within a single day.

**That is a workshop paper or a well-cited engineering report, not a conference submission.** Sizing
it honestly now is cheaper than having a reviewer size it later, and the remaining claims have the
property that matters: each is checked, and none is a category somebody else already owns.

### What the paper must now concede in its first two pages

Conceding late reads as being caught. Conceding first reads as knowing the field.

- OAP, PCAS and PayBench, by name, with what each does better.
- That pre-execution deterministic authorization is an established category with independent
  implementations.
- That this benchmark is smaller, author-written, and lacks matched benign scenarios.
- **SPKI/SDSI (1996), macaroons, object-capability membranes, and arXiv:2605.24036's mechanised
  proof** — narrowing-only delegated authority is thirty years old and machine-checked. The paper
  claims attribution *of* the clamp, never the clamp.
- That the latency comparison is not like-for-like: ~170 µs in-process against OAP's 53 ms p50
  cloud / 174 ms local. **Those numbers measure different things** and presenting them side by side
  without saying so would be the most easily caught dishonesty available.

## Contribution statement — superseded 2026-08-21 draft, kept

The version below was written before the benchmark survey and is retained because the revision
above only makes sense next to what it replaced.

<details>
<summary>The three claims as they stood on 2026-08-21</summary>

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

</details>

## Structure

| § | Content | Source |
|---|---|---|
| 1 | **Introduction.** Agents can pay; payment rails do not govern the payer. x402: 75.41M transactions and $24.24M in 30 days — a **$0.32 average** — with no buyer-side authorization specified | x402.org, verified 2026-08-21 |
| 2 | **Why irreversibility changes the controls.** No chargeback, no recall, no issuer. Detective controls buy a description of a loss rather than a recovery, so the control point moves to *before* | `docs/stablecoins.html` |
| 3 | **Related work, conceding the surface — and now the category.** OAP, PCAS, PayBench first and by name, because they are contemporaries doing the same job; then XACML/OPA/Cedar, macaroons, Certificate Transparency, card controls, Microsoft AGT, transaction monitoring. **This section is why the narrow claim is credible, and it is now longer than the contribution** | [`prior-art.md`](../prior-art.md) §3a, §3b |
| 4 | **Definition.** An AEGL renders a deterministic, attributable verdict on a proposed economic action before execution, and emits evidence sufficient to reconstruct which control produced it. **Includes card authorization systems, deliberately** | `PLAN.md` |
| 5 | **Attribution, and the order asymmetry.** The verdict is order-independent; the attribution is not. Dispositive controls. Why this must be *required* and *scored*, not optional | AEGS VERD-4/4a |
| 6 | **The scoring rule, and the instrument under it.** Why `DEFENDED_BY_ACCIDENT` is a finding rather than a pass — the one part no surveyed system has. 18 attacks, four outcomes, 15/1/2/0. **Concedes in the same section**: smaller than OAP's CTF, author-written, and no matched benign scenarios | EXP-010, [`prior-art.md`](../prior-art.md) §3b |
| 7 | **Two case studies in bounded-not-eliminated.** Count envelopes: unbounded → bounded by a chosen number. Anchoring: truncation detectable *beyond the last publication*. **Both include the vector that asserts the limit** | EXP-009, EXP-010, EVID-6a |
| 8 | **What the measurements cost.** ~170 µs p50 over ten runs, **range 139–330**, zero tokens. Includes the story of the single-run 128 µs that sat below its own distribution's minimum | EXP-007 |
| 9 | **Limitations.** Own-author benchmark (W6.4); **no benign twins, so blanket refusal would score 18/18** — a defect found by reading PayBench rather than by testing; structuring open; anchoring bounded; no independent implementation; one rail; regulatory obligations fall on issuers, not on a library | [`claims-register.md`](../claims-register.md) §3, [`prior-art.md`](../prior-art.md) §3b |
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

**Nothing. All three gates cleared, and two of them changed the paper.**

- ~~`prior-art.md` §4, the two highest-risk surveys.~~ **Done 2026-08-21.** Certificate Transparency
  **refuted** the anchoring novelty; ISO 8583 **strengthened** the attribution claim by supplying
  the objection and the reason it does not apply here.
- ~~A real literature search for existing benchmarks.~~ **Done 2026-08-28, and it was the expensive
  one.** OAP, PCAS and PayBench all exist, all 2026. The claim to a first benchmark is dead, the
  attribution claim narrowed again, and a fourth claim — the delegation clamp — became available
  because the closest system lists it as unformalised in its own limitations.
- ~~P0.1.~~ **Done.** The benchmark has its own page, the score and both open findings are on the
  README, and the sealed lineage is presented as provenance.

**Drafting is unblocked.** The next unit of work is prose against the revised contribution
statement, not more survey — with the one caveat that `prior-art.md` §4 still lists five adjacent
fields as `open`, and capability-based security is the one most likely to touch claim 2.

## Deliberately not in this paper

The x402 proposal. Different reader, opposite virtues — see [`../README.md`](../README.md). The
proposal should cite this paper, not contain it, and it should come after the U3 contributions have
earned the standing to be read.
