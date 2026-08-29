# Which control decided? Required attribution in pre-execution payment governance

**Draft — §1–§7 of 10, 2026-08-28.** Structure and claims from [`outline.md`](outline.md), revised
the same day after three prior-art surveys removed three claims. Every number cites a sealed record
or a dated external reading. §9, the union of limitations from every record cited, is outstanding —
but the limitations that bear on the instrument are stated in §6.2 rather than deferred to it, so a
reader meets them next to the score rather than after it.

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

## 5 · Attribution, and the order it forces

This is the paper's principal claim, and it can be stated as a single observation about
narrowing systems.

### 5.1 The verdict is order-independent; the attribution is not

Take a layer whose controls may only *narrow* a standing verdict — each control may make the outcome
stricter and may never make it more permissive. Order the verdicts by severity: `APPROVE`,
`REVIEW`, `ESCALATE`, `REJECT`.

Under narrowing-only composition the final verdict is the **maximum severity any control proposed**.
Maximum is commutative and associative, so **the final verdict does not depend on the order the
controls ran in.** This is a pleasant property and every system in §3 has some version of it.

Now ask a different question: *which control decided?*

Suppose a treasury envelope narrows `APPROVE` to `REVIEW`, and a risk score then narrows `REVIEW` to
`ESCALATE`. Run them in the other order and the answer is still `ESCALATE`. But the control that
*determined* the outcome differs — in one order the last narrowing was risk, in the other it was
treasury.

**So the moment a specification requires attribution, it has acquired an obligation the verdict
never imposed: it must say something normative about evaluation order.** Not because order changes
what happens, but because order changes what the record says about what happened.

That is the asymmetry. It is why attribution is not a free addition to a narrowing system, and it
is why, we suspect, no surveyed system requires it: the verdict is the part that matters
operationally, the verdict is order-free, and it is easy to conclude that order therefore does not
need specifying.

### 5.2 "The last control that narrowed" is well defined, and insufficient

The default attribution rule is *the last control that narrowed the verdict*, and it is well defined
precisely because widening is impossible. A control proposing something no stricter than the
standing verdict changes nothing, so it did not narrow. The final narrowing is therefore unique.

**The rule is a good default and it fails on a case that matters.** Consider a sanctioned
counterparty whose payment a spending limit also refuses. The limit narrowed. The sanctions
screening did not — the verdict was already `REJECT` when it ran. Under the default rule the record
attributes the refusal to the **budget**.

That record says an agent was stopped by a spending limit. The truth is that it tried to pay a
sanctioned party. An operator who responds by raising the limit finds the payment still refused,
with nothing on the record explaining why.

**Some findings are categorical rather than quantitative.** A counterparty is barred or it is not,
and that does not become less true because a second constraint happened to bite first. So a
specification that requires attribution must also let an implementation declare certain controls
**dispositive**: their finding determines attribution whenever it is *present*, whether or not it
narrowed anything.

This clause exists because the earlier version was wrong and a conformance vector caught it. We
report that rather than presenting the final rule as though it were the first one, because a
specification whose errors are visible is easier to trust than one whose history is not.

### 5.3 Declaration is what stops this being an escape hatch

An implementation free to nominate any control as dispositive after the fact can attribute a
decision to whatever is convenient. Two requirements prevent that:

- the set of dispositive controls and **their precedence relative to one another** must be fixed in
  advance and in writing;
- the evaluation order must be **documented**, not fixed by the specification.

The second is deliberate and slightly uncomfortable. A standard cannot impose a sequence, because it
does not know which controls a given implementation has. But an implementation whose order is
undocumented has an attribution nobody can predict, and therefore **an attribution nobody can
audit** — which is the entire failure this section exists to prevent.

There is a consequence worth naming: a dispositive control must record its finding
*unconditionally*, because attribution now depends on the finding being present rather than on its
having changed the outcome. A control that stays silent when it did not narrow cannot be
dispositive.

### 5.4 Attribution on permit, which no surveyed system requires

Every system in §3 that attributes at all attributes a **refusal**. OAP's reason codes attach to
`DENY`. This is the natural place to start: a refusal demands an explanation because somebody is
inconvenienced by it.

**A permit is the more interesting record.** *"This payment was approved, and the control that let
it through was the budget envelope with $12.40 of headroom"* answers a question a refusal record
cannot: **would deleting this control have changed anything observable?** A layer whose controls all
silently permit is indistinguishable from a layer with no controls at all, and the only way to tell
them apart from the outside is to require the permit path to name its decider too.

### 5.5 The property this buys, stated as a test

The reason to require attribution rather than encourage it is that it converts an untestable
assurance into a testable one.

> **Delete a control. Does any record change?**

If the answer is no, that control was decorative and its removal is invisible to every audit. This
is checkable by a third party holding only the record format and a set of vectors — no access to
the implementation, no cooperation from its author. That is what "independently scored" means here,
and it is the part §3.5 identifies as unclaimed.

---

## 6 · The scoring rule, and the instrument under it

### 6.1 `DEFENDED_BY_ACCIDENT`

An adversarial benchmark of a *control layer* normally has two outcomes per attack: the attack
succeeded, or it did not. We use four, and the third is the contribution:

| Outcome | Meaning |
|---|---|
| `DEFENDED` | Refused, by the control the attack targets |
| `DEFENDED_BY_ACCIDENT` | Refused, by a control that was not aiming at this attack |
| `UNDEFENDED` | Not refused |
| `ERROR` | The attack did not execute |

**`DEFENDED_BY_ACCIDENT` is scored as a finding, not as a pass**, and the reason is that a
coincidence has no maintenance contract. A trust-farming attack refused by a risk score that
happened to fire is refused today and may not be refused after an unrelated weight is retuned. The
record will not show a regression, because nothing that was ever asserted stopped being true.

Requiring attribution (§5) is what makes this outcome *observable*. Without a record naming the
control that refused, an accidental defence and an intentional one look identical from the outside —
which is the practical argument for claim 1 restated as a measurement.

No system surveyed in §3 has this outcome. OAP records a deny code but does not ask whether that
code was the one aiming at the attack; PayBench scores whether a refusal was appropriate, not where
it came from.

`ERROR` is separated from the other three for a reason found the hard way: an attack with no handler
silently reports nothing, and a suite full of errors looks like a clean run to anyone reading only a
failure count. A test asserts every attack executed.

### 6.2 The instrument, and what is wrong with it

Eighteen attacks across four classes — numeric, economic, evidence, authority. The current score is
**15 defended, 1 by accident, 2 undefended, 0 errors**, recorded in a sealed experiment record with
a checksum. A test compares a live run against that record and **fails on any difference in either
direction**: a closed gap is as much a deliberate change as a regression, and both must be committed
with the record updated.

Three properties of the instrument we state here rather than in the limitations section, because a
reader should not have to reach §9 to learn them:

**It is smaller than the alternatives and it is not externally attacked.** OAP's CTF produced 4,437
adversarial decisions across 1,151 sessions with external participants. Ours has eighteen attacks,
all written by the author of the system under test. On the axis of independence, we are behind the
work we are citing.

**It has no benign twins.** PayBench pairs each trap scenario with a lookalike that is safe to
permit, so an agent that refuses everything cannot score well. **We have no such pairing.** An
implementation that refused all eighteen attacks would score 18/18 on our instrument, which means
the instrument does not measure over-refusal at all — the failure mode §2 argues is expensive on an
irreversible rail. This is a genuine defect and it was found by reading a competitor's design rather
than by testing our own.

**Two findings are open and stay open.** Structuring is bounded rather than refused, for reasons
given in §7. Journal truncation is closed only against an external anchor, and no anchor ships by
default, so the benchmark reports the posture an installer actually gets rather than the one
available to a careful operator.

### 6.3 The lineage, including a wrong measurement

The record chain behind the score is `EXP-008 → EXP-009 → EXP-010`. `EXP-009` **supersedes**
`EXP-008` because a measurement in it was wrong: an attack was parameterised over a window its
target control could not observe, so the result described the parameterisation rather than the
control.

The superseded record was not edited. It remains, marked superseded, with the reason attached.

We include this because a record lineage containing a correction is better evidence about method
than a clean one. A benchmark whose history shows no errors is either very carefully run or very
carefully tidied, and a reader has no way to tell which.

---

## 7 · Bounded, not eliminated

The third claim is a specification obligation: **where a control bounds a risk rather than
eliminating it, the specification must require the implementation to say so.**

This is unusual. Standards ordinarily specify what a control must *do*. The clause here specifies
what an implementation must *admit* about the residual its control leaves behind — and both cases
below ship with a conformance vector that asserts the limit, so the admission is scored rather than
narrated.

### 7.1 Count envelopes: unbounded becomes bounded-by-a-number

A rate limit bounds how *fast* an agent acts. A value envelope bounds how *much* it spends. Neither
bounds **how many times it acts over a window longer than the rate limit's**, and nothing multiplied
*trivial* by *many* and compared the product to anything.

The measured consequence: an agent pacing at **97 actions an hour — three per cent under a ceiling
of 100 — was compliant indefinitely**, at 2,328 actions a day for $2.33 against a $50 daily budget.
Every value envelope was out of reach because each action was trivial. Every rate limit was out of
reach because the pacing sat under it.

A cumulative count envelope closes it: the paced-evasion attack moved from undefended to defended,
refused at action 500 and attributed to the treasury control citing `actions_per_day`.

**What it does not do is eliminate structuring**, and the specification requires saying so. Forty
payments of $0.001 five minutes apart total $0.04 and are nowhere near 500 actions. The envelope
bounds the mechanism at a number the operator chose; it does not refuse this instance.

**And it should not.** Forty trivial purchases in an afternoon is also what a legitimate agent does.
A control that refused it would be producing a false positive on an irreversible rail, which §2
argues is a real cost rather than a safe default. The honest statement is *bounded at a number you
chose, not eliminated* — and the attack remains in the benchmark as `UNDEFENDED` rather than being
reclassified.

### 7.2 Anchoring: detectable, beyond a bound the operator chose

A hash chain detects edits and cannot detect truncation of its own tail, because **any prefix of a
valid chain is itself a valid chain.** The missing information is *that there was more*, and no
amount of internal linking supplies it.

An external anchor supplies it: a `(length, head)` commitment published where the journal's writer
cannot reach. This is Certificate Transparency's signed tree head applied to a spend journal, and
§3.4 records that the survey establishing this refuted the novelty we had claimed for the mechanism.

**The bound is the honest part.** An anchor is published at some cadence, so everything appended
since the last publication is unattested and remains silently truncatable. Anchoring does not make
truncation detectable; it makes truncation detectable **beyond a bound the operator chose**. A
vector asserts the difference rather than describing it.

Verification therefore has four outcomes, not two: `consistent`, `truncated`, `diverged`, and
`unknown` — and **`unknown` is never a pass.** An anchor that cannot be read is a fact about the
anchor, and reporting it as agreement would let anyone able to partition the verifier from the sink
also make the journal verify.

No anchor sink ships with the implementation. An append-only file beside the journal is that journal
at one remove in any deployment where the agent's own host can rewrite it, and shipping one would
make the gap *look* closed.

---

*§8–§10 not yet drafted. §8 is what the measurements cost; §9 the union of limitations from every
sealed record cited; §10 the open question of whether a governance standard can be validated by
anyone other than its author.*
