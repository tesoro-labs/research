# Prior art — the novelty test, done properly

**Started:** 2026-08-21 · **Status:** first pass. Confidence marked per item; `recalled` entries
must be verified against a primary source before publication.

The purpose of this document is to **make the novelty claim smaller**. A paper that concedes seven
things and defends one survives review; a paper that claims a new category does not. Every entry
below either kills a claim, narrows it, or leaves it standing with a reason.

**Confidence key:** `verified` — a primary or authoritative source was read while writing this.
`recalled` — from training data, plausible, **not yet checked**. `open` — not investigated.

---

## 1 · Claims this survey kills outright

| Claimed as novel | Prior art | Confidence |
|---|---|---|
| A governance layer that decides whether an agent may act | Microsoft Agent Governance Toolkit — own specification, conformance suite, five languages, 6,042 stars, built independently | `verified` — tree and files read 2026-08-20 |
| Deterministic policy evaluation over structured facts, no model in the path | XACML (OASIS, 2003→3.0), OPA/Rego, Cedar | `verified` for XACML 3.0; `recalled` for Cedar specifics |
| Cumulative spend limits per period, per merchant, per category | Corporate card controls and spend-management products. Predates all of this by decades | `recalled` — needs one citable source |
| Delegated authority that narrows at each hop | **Macaroons** — bearer credentials with caveats that monotonically attenuate authority. This is exactly the delegation clamp | `recalled` — Birgisson et al., NDSS 2014. **Verify venue and title before citing** |
| Append-only hash-chained log with an external anchor | Certificate Transparency (RFC 6962), Trillian, Sigstore/Rekor witness networks, AWS QLDB | `recalled` — RFC number needs checking |
| Four-valued logic for "we do not know" | Kleene three-valued logic; SQL `NULL` semantics | `verified` conceptually, trivially true |
| Fail-closed on an undischargeable requirement | **XACML 3.0 obligations**: a conforming PEP must *deny* unless it can discharge every obligation attached to the applicable policy | `verified` |

That last row deserves attention rather than a shrug. **XACML already has a fail-closed conformance
rule of the same shape as "unknown is never a pass."** The parallel is close enough that the paper
should cite it as precedent *for* the design rather than pretend the idea is new. Precedent is an
argument in favour; silence about precedent is a weakness a reviewer finds.

---

## 2 · The central claim, narrowed by what the survey found

**Claim as originally stated:** *attribution — which control decided — is a novel normative
requirement.*

**What XACML 3.0 actually provides** (`verified`): a PDP returns `Permit` / `Deny` /
`NotApplicable` / `Indeterminate`, and a response **may** include a `PolicyIdentifierList` naming
the policies that applied. So *"which policy decided"* is **expressible in a 2003-lineage
standard** and has been for twenty years.

**Therefore the claim cannot be "nobody reports which rule decided."** It has to be narrower, and
these are the parts the survey did **not** find prior art for:

1. **Attribution as a *required* output rather than an optional one.** XACML's
   `PolicyIdentifierList` is optional; a conforming PDP may omit it entirely.
2. **Attribution as an independently *scored* conformance property** — test cases that pass or fail
   on *which control* was named, separately from whether the verdict was right. This is the part I
   believe is genuinely absent, and the part the paper should lead with.
3. **A normative evaluation order justified by the asymmetry** that the *verdict* is
   order-independent while the *attribution* is not. XACML has rule/policy combining algorithms
   which fix precedence, so ordering is not new; **the stated justification** — order matters
   because attribution matters, not because the outcome would change — is what I have not seen.
4. **Dispositive controls** — a finding that determines the verdict regardless of evaluation order
   or other controls' proposals.

**Recommended claim wording for the paper:**

> Access-control standards have long been able to *report* which policy applied. We make attributed
> decision a **required and independently conformance-tested** property of an economic governance
> layer, and show that doing so forces a normative evaluation order even where the verdict itself is
> order-independent.

That is defensible. *"We invented attribution"* is not.

**Open work:** check whether any OPA/Rego or Cedar conformance suite scores decision provenance;
check the NIST AI RMF and EU AI Act traceability requirements, which may impose something
attribution-shaped and would be a strong supporting citation rather than a competitor.

---

## 3 · Claims still standing after this pass

### (a) A reproducible adversarial benchmark for pre-execution economic governance

**Searched for:** an existing benchmark for agent spend governance. **Not found** (`open` — one
pass only; needs a proper literature search before the paper asserts absence).

What exists nearby: OWASP Agentic Top 10 (a *taxonomy*, not an executable benchmark);
Microsoft AGT's 992 conformance tests (conformance to *their* spec, not adversarial); AgentBench,
AgentHarm and similar (capability and harm benchmarks for model behaviour, **not** economic
controls) — all `recalled`, all needing verification.

**Why it stands:** the artefact is not "we tested our thing." It is 18 attacks with four outcomes
where `DEFENDED_BY_ACCIDENT` — *refused by a control the attack does not target* — is counted as a
**finding rather than a pass**, plus a record lineage (EXP-008 → EXP-009 supersedes → EXP-010) in
which a wrong measurement was corrected by superseding rather than editing. That scoring rule and
that provenance discipline are the contribution; the 18 attacks are the instrument.

**Weakness to state, not hide:** every attack was written by the author of the system under test.
This is recorded as W6.4 and it is the single biggest hole in the claim.

### (b) "Bounded, not eliminated" as the unit of a governance promise

**Standing, with a caveat.** The *idea* that a control bounds rather than eliminates is not new —
it is ordinary risk management, and rate limiting has always been understood this way.

What appears to be new is applying it as a **disclosure discipline in a specification**: `ENV-7`
and `EVID-6a` both require the implementation to state the residual, and vectors *assert the
limit* rather than the capability — `anchor-truncation-inside-the-window-is-undetected` expects
`consistent`, which is correct and is what "beyond a bound you chose" costs.

**Nearest prior art to check** (`open`): RFC 3552-style security-considerations conventions, and
whether any standard *requires* a residual-risk statement as a conformance item.

### (c) The four-state rule extended to the governance layer's own availability

*Absent degrades; broken raises.* Supporting rather than headline. Nearest prior art is fail-safe
vs fail-secure design (`recalled`, decades old) — the narrow part is applying the distinction to
*the control layer's own import failure*, found because a missing chart library switched governance
off and reported it under the governance layer's name.

---

## 3a · The two highest-risk surveys, done 2026-08-21

Both were flagged as able to kill a claim. **One shrank a claim; the other strengthened it and
supplied an argument the paper was missing.**

### Payment authorization already has the field — and deliberately does not populate it

`verified`. ISO 8583 carries a response code in **data element 39**, and card networks therefore
*can* report why a transaction was declined. Some codes are specific: insufficient funds, exceeds
withdrawal limit, expired card.

**But code 05, "do not honour", is a deliberate catch-all**, and the reasons given for keeping it
vague are not laziness:

- revealing specific decline reasons would let fraud-detection systems be **reverse-engineered**;
- specific reasons can disclose **sensitive cardholder information**;
- generic responses prevent internal **risk models** from being inferred.

Its overuse is documented and criticised — Spain, Brazil and the USA are named as having
disproportionate rates — and a merchant cannot diagnose the cause from their side at all.

**This does not kill the attribution claim. It supplies the objection the paper has to answer**, and
answering it is a contribution in itself:

> Card networks can attribute a decline and choose not to, for principled reasons. Why is required
> attribution safe in an economic governance layer?

**Because the reader is different.** In a card network, attribution flows to the **merchant** — a
counterparty with an incentive to probe the issuer's risk rules. In an AEGL, attribution flows to
the **operator who wrote the policy and owns the budget**. There is nothing to reverse-engineer:
telling them *"refused by `daily_usd`"* discloses a number they authored. No third party's privacy
is involved, because the agent's own operator is the audience.

**And the boundary that follows is already in the implementation.** Where attribution *would* reach
a counterparty, the card-network reasoning applies in full and the detail must be withheld —
identity is pseudonymous by default, and *"telling a seller your remaining budget invites it to
charge exactly that."* The two disciplines are the same rule pointed in opposite directions, which
is the version of this argument worth publishing.

**Still open:** whether EMV or any card-scheme rule *requires* accuracy in DE 39. If one does, the
"not required anywhere" half of the claim needs softening.

### Certificate Transparency already has the mechanism, and this shrinks EVID-6a

`verified`, and this is the finding that costs something.

CT's **Signed Tree Head** carries a **tree size** and a root hash. That is `(length, head)` — 
*exactly* what `AEGS-0.1-EVID-6a` requires an anchor to commit to, and for the same reason. On top
of it CT has:

- **consistency proofs** — a logarithmic number of hashes proving one snapshot is a prefix of
  another, which is truncation and omission detection;
- **witness networks** — independent parties gossiping to confirm a log is append-only and to detect
  **split-view attacks**, which is external anchoring by another name;
- **a defined client rule** — on receiving an STH with a different tree size, fetch a consistency
  proof and keep the larger only if it verifies.

**So the mechanism in `EVID-6a` is Certificate Transparency's, applied to a spend journal.** The
paper must say that in the related-work section rather than let a reviewer discover it.

What survives, and it is narrow:

1. **Requiring it in a governance standard**, where the artefact being anchored is a record of
   refusals rather than of certificates.
2. **The four-outcome result type, with `unknown` never a pass.** CT clients handle an unreachable
   log, but I have not found the outcome *named and normatively separated* from consistency — that
   distinction is what stops a verifier who can be partitioned from the sink from reporting success.
3. **A different adversary.** In CT the *log operator* misbehaves and there are many clients. Here
   the *journal writer is the agent under governance*, and there may be exactly one operator, so
   gossip between peers is unavailable and the anchor must be a party the writer cannot reach.

**Recommended wording change:** stop describing anchoring as a contribution. Describe it as
*"CT's STH-and-witness model, required by a governance specification, with the unavailable case
named as its own outcome."* That is defensible and considerably smaller than what was implied
before this survey.

---

## 4 · Adjacent fields to survey before publication

Each could contain a paper that weakens a claim. None checked yet.

| Field | Why it matters | Status |
|---|---|---|
| Capability-based security | Macaroons, SPKI/SDSI, object capabilities. The delegation clamp lives here | `open` |
| Transparency logs | CT, Trillian, witness/gossip protocols | **`verified` §3a — the mechanism is CT's. Claim shrunk** |
| Payment authorization | ISO 8583, EMV, 3-D Secure | **`verified` §3a — the field exists and is deliberately vague. Claim strengthened.** EMV accuracy requirements still `open` |
| Transaction monitoring / AML | Structuring detection is a solved commercial problem. Ours is deliberately deterministic; theirs is not | `open` |
| Budget/quota systems | Cloud quotas, FinOps, Kubernetes ResourceQuota. Count *and* value envelopes over windows | `open` |
| Agent governance | Microsoft AGT covered. Others unknown | partly `verified` |
| AI governance frameworks | NIST AI RMF, EU AI Act traceability. Likely *supporting* citations | `open` |

**The two marked highest-risk are the ones to do first.** If transparency-log literature already
formalises the four anchor outcomes, `EVID-6a`'s contribution shrinks to "applied to a spend
journal." If ISO 8583 or EMV already specify attributed pre-execution authorization with required
provenance, the central claim needs rewriting rather than narrowing.

**Finding that out early is the point of this document.** It is much cheaper to discover it here
than in review.

---

## 5 · What this survey has already changed

1. **The AEGL definition narrowed** and now deliberately includes card authorization systems —
   see the workspace plan (internal). An AEGL is the agent-native instance of a known pattern.
2. **The attribution claim narrowed** from "novel" to "required and conformance-scored," because
   XACML can already report it optionally.
3. **XACML obligations became a supporting citation** rather than an unmentioned neighbour.
4. **Two survey items are flagged as able to kill a claim** rather than left as background reading.
