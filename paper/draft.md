# Which control decided? Required attribution in pre-execution payment governance

**Draft — §1–§4 only, started 2026-08-28.** Structure and claims from
[`outline.md`](outline.md), which was revised the same day after three prior-art surveys removed
three claims. Every number here cites a sealed record or a dated external reading; see §9 (not yet
drafted) for the union of limitations from every record cited.

---

## 1 · Introduction

An agent that can pay is an agent that can overpay, and the rails it pays over do not govern the
payer.

The scale is measured rather than projected. On 21 August 2026 the x402 protocol reported **75.41
million transactions and $24.24 million of volume over 30 days** — a **$0.32 average payment** — on
a protocol whose own documentation specifies no spend limits, no buyer-side authorization, and no
governance layer. A settlement rail is not required to have opinions about whether a payment should
happen. It is required to make it happen, and it does.

That leaves a gap that is easy to describe and awkward to fill. The seller is protected by getting
paid. The chain is protected by finality. **Nobody in the transaction is positioned to ask whether
the buyer should have bought**, because the only party with that interest is the buyer's principal,
who is not present at the moment of payment and may not learn of it for hours.

This paper is about the layer that occupies that position, and about one property that layer should
be required to have and mostly is not.

### The category is not new, and saying so early is the point

Three systems published in 2026 place a deterministic decision before an agent's action. **OAP**
intercepts tool calls at the framework layer and returns `ALLOW`, `DENY` or `ESCALATE` from a signed
policy pack, with an Ed25519 decision record per call [Uchibeke 2026]. **PCAS** compiles policy into
a Datalog-derived reference monitor and reports moving policy compliance from 48% to 93% across
frontier models. **PayBench** benchmarks agents holding delegated payment authority across 226
scenarios built as 113 matched trap/lookalike pairs [Plunkett 2026].

OAP's own discussion observes that it and PCAS *"independently converge on the need for
deterministic pre-action enforcement as a distinct architectural layer … This convergence suggests
the category is real, not an artifact of a single system's design."*

**We agree, and we are the third data point rather than the first.** A paper introducing this
category would be introducing something with several independent implementations. What follows is
therefore not a proposal for a layer. It is an argument about one output that layer should be
obliged to produce, and evidence that the obligation is currently absent.

### Contribution

1. **Attribution as a required and independently scored output** — the record must name the control
   that decided, on **permit** as well as on refusal; must resolve **which** control is reported
   when several would have refused; and must name the step that limited a delegated authority.
   Requiring it forces a normative evaluation order even though the verdict itself is
   order-independent (§5).
2. **"Bounded, not eliminated" as a disclosure obligation** — a specification clause requiring an
   implementation to state the residual its control leaves behind, with two worked cases (§7).
3. **A scoring rule**, `DEFENDED_BY_ACCIDENT`: in an adversarial benchmark of a control layer,
   counting *refused by a control the attack does not target* as a finding rather than a pass (§6).

These are small. Three prior-art surveys removed three larger claims, one of which we invented and
withdrew within a day, and §3 reports what each removed. We think the remaining three are correct
and unclaimed, and we would rather defend three narrow things than lose an afternoon of a reviewer's
time to a fourth.

---

## 2 · Why irreversibility moves the control point

The controls in this space look unusual until the settlement properties are stated, after which they
look forced.

A card payment is a promise that can be broken. Authorization, clearing and settlement are separate
events; a cardholder can dispute; an issuer can charge back; a network can reverse. This gives the
whole system a property that shapes every control built on it: **a detective control still works.**
Finding a fraudulent transaction on Tuesday can undo a payment made on Monday, so it is rational to
invest heavily in monitoring, scoring and review after the fact.

A stablecoin transfer on a public chain has none of that. There is no chargeback, no recall, and no
issuer standing behind the payer. Once the transaction is final, a control that notices a problem
has produced **a description of a loss, not a recovery.**

Two consequences follow, and they are the reason this layer is shaped as it is.

**The control point moves to before execution.** Not because pre-execution controls are better in
general — they are worse in one important way, discussed below — but because after execution there
is nothing left for a control to do except write things down.

**A refusal costs something and must be accounted for.** A control that refuses a legitimate payment
on an irreversible rail has not merely inconvenienced anyone; it has failed to buy something the
principal wanted, and there is no dispute process to correct it. This cuts directly against the
instinct to refuse when uncertain, and it is why the benchmark in §6 treats over-refusal as a defect
rather than as caution — and why, in §9, we report that our own instrument fails to measure it.

**The honest cost of moving early.** A pre-execution control decides on less information than a
post-hoc one. It cannot see whether the goods arrived, whether the counterparty later proved
fraudulent, or whether the same pattern repeated across a hundred other principals. Systems that
monitor after the fact see all of that. **We are not claiming the earlier control is more accurate.
We are claiming it is the only one whose output can still change the outcome**, and that this makes
the accuracy trade a forced one rather than a chosen one.

---

## 3 · Related work, and what each survey removed

This section is longer than the contribution it supports. That ordering is deliberate: three
surveys removed three claims, and the credibility of what is left rests on showing the removals
rather than the survivors.

### 3.1 Contemporary pre-action authorization

**OAP** [Uchibeke 2026] is the closest work. It is deterministic (*"Same inputs, same decision. No
sampling, no temperature"*), bypass-resistant by running at the framework layer rather than in the
model's reasoning, fail-closed, and auditable — every decision produces a signed, timestamped
record. Denials carry a structured reason code such as `oap.limit_exceeded` or
`oap.merchant_forbidden`, plus a human-readable explanation. It was evaluated against **4,437
adversarial decisions across 1,151 attack sessions** in a live capture-the-flag against a banking
agent, with external participants.

**That last figure is better than anything we report**, on the axis we identify in §9 as our
weakest: our attacks were written by the author of the system under test, and OAP's were not.

OAP's own limitations record that it does not formalise a delegation model (*"planned for v1.1"*),
that its `ESCALATE` path is specified but unimplemented in the reference, and that attack
sequence-based structuring is future work.

**PCAS** compiles policy to a Datalog-derived reference monitor, permitting recursive rule
composition where OAP trades expressiveness for constant-time evaluation. **PayBench** [Plunkett
2026] benchmarks agent behaviour under three control conditions — no policy, prompt-based policy,
hard tool constraints — using matched trap/lookalike pairs so that blanket refusal cannot score
well. **EcoAgent-Bench** scores agents' economic decision *quality* under budget constraints rather
than enforcement. **Faramesh** is an execution-time control plane; **ToolMisuseBench** is an
offline deterministic harness isolating failure origin between call construction, policy handling
and recovery.

### 3.2 Policy languages and authorization

**XACML 3.0** responses **may** carry a `PolicyIdentifierList`, so *"which policy decided"* has been
expressible in a 2003-lineage standard for two decades. **OPA** and **Cedar** are the modern
expression of policy-as-data. Our claim is therefore not that attribution is inexpressible or
unprecedented; §3.5 states what remains.

### 3.3 Capability-based security — and the claim it removed

**SPKI/SDSI** (1996) provides authorization certificates that delegate, and a reduction algorithm
computing effective authority through a certificate chain. **Macaroons** (2014) provide caveat
attenuation. The **object-capability** model provides attenuating proxies and the **membrane**
pattern for transitive attenuation. Intent-Driven Computing [arXiv:2605.24036, 2026] proves that
*"capabilities can only narrow, never widen, through composition"* with a mechanised Coq proof.

An earlier version of this paper claimed a narrowing-only delegation clamp as a contribution, on the
basis that OAP lists delegation chains as unformalised. **That was true about OAP and wrong about
the field, and the claim is withdrawn.** Narrowing-only delegated authority is a thirty-year-old
standard with a machine-checked proof.

What the surveyed work computes or proves is the *result* of attenuation. None of it names **the
step that produced the result** — and that is an attribution property, not a delegation one, so it
appears in claim 1 and is not counted separately.

### 3.4 Transparency logs — and the claim they shrank

**Certificate Transparency** commits a log to a signed tree head, which is exactly a
`(length, head)` pair over an append-only structure. Our evidence anchoring is that mechanism
applied to a spend journal. The survey that established this **refuted** the novelty we had claimed
for it; the clause survives as engineering, not as contribution.

### 3.5 What is left after all of it

Every surveyed system that attributes at all attributes a **refusal**. OAP's reason codes attach to
`DENY`. XACML permits a policy identifier in a response but requires nothing. None of the surveyed
work:

- requires the record to name the control that **permitted** an action;
- defines **precedence** when several controls would each have refused, so that the reported control
  is determined rather than incidental;
- makes the presence of attribution **independently scoreable** by a third party holding only
  machine-readable vectors and no access to the implementation;
- states the **order asymmetry** — that the verdict is order-independent while the attribution is
  not, so requiring attribution forces a normative evaluation order.

Those four are claim 1.

### 3.6 Adjacent work not surveyed

Transaction monitoring and AML systems, cloud and FinOps quota systems, NIST AI RMF and EU AI Act
traceability, and agent governance frameworks beyond Microsoft's Agent Governance Toolkit remain
**unsurveyed at the time of writing**. We do not believe they touch the three surviving claims. We
believed the same about capability-based security on the morning of the day it removed one.

---

## 4 · Definition

> An **autonomous economic governance layer** renders a deterministic, attributable verdict on a
> proposed economic action **before that action is executed**, and emits evidence sufficient to
> reconstruct which control produced the verdict.

Four elements, each doing work.

**Deterministic.** Same inputs, same verdict, replayable from the record. This excludes a model
sampling at temperature above zero from the decision path. It does not exclude a model from the
system: an advisory component may *narrow* a verdict and may never widen one, which keeps the
decision reproducible while allowing judgement to make it stricter.

**Attributable.** The record names the control that produced the verdict. This is the property the
paper argues should be required, and §5 is about what it costs.

**Before execution.** The verdict is rendered while refusal is still free. After execution a control
can only describe.

**Evidence sufficient to reconstruct.** Not a log line asserting a conclusion, but enough state to
re-derive it — the inputs, the policy identity, and the control that decided.

### The definition deliberately includes card authorization

A card authorization system satisfies every element. It decides before the money moves, it decides
deterministically from rules the issuer set, it returns a reason code, and it keeps a record.
**ISO 8583 has carried a decline-reason field since the 1980s.**

We consider this a feature of the definition rather than a flaw in it. A definition of *governance
layer* that excluded the most widely deployed governance layer in the world would be a definition
built to make its author's system look novel. **The interesting question is not whether card
authorization qualifies — it does — but what changes when the payer is software acting under
authority conferred earlier, on a rail with no chargeback, at a rate no cardholder generates.**

That framing also supplies the strongest objection to claim 1, from the same source. Card networks
deliberately **do not** tell the cardholder which rule declined them, because a declined fraudster
who learns the rule can work around it. Attribution is a genuine security cost, not a free good.

Our answer is narrow and depends on who reads the record: **in this setting the reader is the
operator who wrote the policy.** A principal reading their own agent's refusal is not an adversary
probing an issuer's fraud model; they are the party who set the limit and now need to know which
limit bound. Where a record is disclosed to a counterparty, that is a different audience and the
projection is different — the layer described here discloses a strict subset to a seller and never
includes which control decided.

---

*§5–§10 not yet drafted. §5 is attribution and the order asymmetry; §6 the scoring rule and the
instrument under it; §7 the two bounded-not-eliminated cases; §8 measurement cost; §9 limitations;
§10 the open question of whether a governance standard can be validated by anyone other than its
author.*
