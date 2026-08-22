# The gap: agents transacting through obliged entities

**Written:** 2026-08-22 · **Primary source:** *Stablecoin compliance in 2026: which rules apply to
your business*, Sumsub, 66pp · **Cross-checked against:** the GENIUS Act timeline (verified
independently), x402 volumes (x402.org, 2026-08-21)

The question this answers: **what exists between a stablecoin compliance programme and an
autonomous agent that spends, and is anything actually missing?**

---

## 1 · What the guide covers, precisely

Seven frameworks: **FATF Recommendation 16** (the Travel Rule), the **GENIUS Act** (US), **MiCA**
(EU), the **FCA cryptoasset regime** (UK), the **MAS single-currency stablecoin framework**
(Singapore), the **HKMA Stablecoins Ordinance** (Hong Kong), and **VARA** (Dubai).

Six business segments, each with a readiness checklist:

| Segment | Who it is |
|---|---|
| Banks and traditional finance | institutions adding stablecoin activity |
| Stablecoin issuers | mint, redeem, hold the reserve |
| Payments and processors | move value for others |
| Infrastructure and custody | custody, and the rails others build on |
| Wallets | custodial and non-custodial |
| Card issuers | cards that spend or settle in stablecoins |

The guide's own conclusion is the useful frame: *"your specific obligations depend on what you do
and where you do it… a single stablecoin payment can involve several of them at once."*

---

## 2 · The observation

**None of the six segments is "an autonomous agent that spends."**

That is not an omission in the guide. It is correct. **An agent is not an obliged entity** — it has
no legal personality, cannot hold a licence, and cannot be a VASP. Nothing in any of the seven
frameworks attaches to it.

**The exposure lands on the obliged entity instead**, and it arrives without a category. A payments
processor, a wallet, a card issuer or a bank whose customers deploy agents inherits transaction
flow their obligations were not written for — and the obligation is still theirs.

The scale is not hypothetical. x402 alone reported **75.41M transactions and $24.24M of volume in
30 days** on 2026-08-21, a **$0.32 average payment**, on a protocol whose own documentation
specifies no buyer-side authorization, no identity and no AML.

---

## 3 · Three assumptions agents break

Each is load-bearing in the frameworks, and each fails in a different way.

### (a) The originator is a person who acted

FATF R.16 requires originator and beneficiary information on qualifying transfers, and the guide's
payments chapter requires applying it *"on every qualifying transfer, in both directions."*

An agent-initiated payment **has** an originator — the human or organisation whose funds move — and
that party **did not initiate the transfer.** They authorised a policy, days earlier, under which
software later decided. The record shows a person who pressed nothing.

Nothing in the Travel Rule payload distinguishes:

- a person who reviewed and sent this payment;
- a person who delegated authority to an agent that sent it under policy;
- a person whose credentials an agent used after being compromised.

**The three are materially different and currently indistinguishable in the record.**

### (b) The customer can be onboarded

KYC, KYB, beneficial ownership, ongoing monitoring — all assume a subject with documents. Sumsub's
own product surface is built on it: ID verification, proof of address, liveness, bank account
verification.

**An agent has no documents.** It is not a customer, not a beneficial owner, and not a synthetic
identity either — a synthetic identity is a fabricated person, and an agent is not pretending to be
one. The existing categories do not contain it.

What *can* be established is **attribution**: which onboarded human or entity is accountable for
this agent's spending, provable after the fact. That is a governance question, not an identity one,
and it is the honest division of labour.

### (c) Behavioural baselines are built from human tempo

Transaction monitoring, structuring detection and velocity rules are calibrated on how people
spend.

An agent making **500 micropayments a day** is either entirely normal or a serious alarm, and
nothing in the transaction stream says which. Absent a declaration that an agent is acting, an
obliged entity faces a dilemma with two bad answers: tune thresholds for agents and lose
structuring detection for humans, or leave them and drown in false positives.

The measured case makes this concrete. A **$0.32 average payment at 75M/month** is, on any
human-calibrated model, either invisible or pathological. Both readings are wrong.

---

## 4 · What actually fills it

Not screening, not identity, not a licence. **Evidence that answers the questions an agent makes
unanswerable.**

| The obliged entity must be able to show | What an AEGL can supply |
|---|---|
| Which accountable human authority this payment was made under | Registered identity with a delegation chain, clamped so a delegate's authority is the narrower of its own and its delegator's |
| That the payment was permitted **before** it happened, not reviewed after | A pre-execution verdict, deterministic, in microseconds |
| **Which control permitted or refused it** | The attributed control — required, and independently conformance-scored |
| That the record has not been edited or truncated | Hash-chained evidence with external anchoring, and the residual stated rather than hidden |
| Whether screening ran at all | **The gap in our own implementation. See §6.** |

The distinction that has to hold, and it is the same one the guide draws for itself:

> **An AEGL consumes compliance signals and produces governance evidence. It does not produce
> compliance signals, and it is not a compliance programme.**

Screening, lists, KYC/KYB, case management and filing belong to the compliance platform. Which
authority an agent acted under, and which control decided, belong to the governance layer. Neither
substitutes for the other.

---

## 5 · Why this is worth a specific profile

The frameworks differ by jurisdiction, but what an obliged entity needs from a *governing agent* is
the same everywhere: attribution, a pre-execution decision, and an evidence trail. That is a
**profile** — the mechanism AEGS already has — not a fork of the standard.

Existing profiles: `aegs-1` (baseline), `aegs-2` (counterparty-aware, extends `aegs-1`), `none`.
Requirements are `MUST_EXERCISE` / `MUST_RECORD` / `OPTIONAL`, each with a `recordPath`.

A `stablecoin-1` profile extending `aegs-2` needs exactly two changes, and the restraint is the
point:

1. **`AgentIdentity: MUST_EXERCISE`** — already so in `aegs-2`. In this vertical it is the whole
   point: without it there is no originator attribution.
2. **`AMLAssessment: MUST_RECORD`** — not `MUST_EXERCISE`.

The second needs defending, because it looks weak. `aegs-1` marks `AMLAssessment` optional with the
note: *"Schema only, no engine anywhere. Requiring it would make the profile unsatisfiable, which
does not raise the bar — it makes the bar decorative."* That reasoning still holds and nothing here
overrides it.

**But `MUST_RECORD` raises a real bar without requiring an engine.** It forces the record to state
whether screening ran — and to distinguish *absent* from *not-run* from *unknown*. An obliged entity
integrating a real provider gets a record proving screening happened; one that has not gets a record
positively stating it did not. **Both are better than a record with silence where screening should
be**, and silence is what exists today.

---

## 6 · The gap in our own implementation

Measured, not assumed. A decision record's `assessments` block currently carries:

```json
"assessments": {
  "trust": { "assessed": true, "score": 0.25, "indicators": ["new_vendor"] },
  "risk":  { "assessed": true, "score": 0.2001, "indicators": ["unknown_vendor"] },
  "roi":   { "assessed": true, "score": null, "detail": "no declared expected value…" }
}
```

**There is no `aml` key.** So a `stablecoin-1` profile requiring `AMLAssessment: MUST_RECORD` is
**unsatisfiable today.**

**I proposed the wrong fix first, and a guard caught it within a minute.** The obvious move is to
emit `assessments.aml = {"assessed": false}` — the record would finally *say* screening had not run
rather than being silent. It looks honest and it is a false statement: `assessed: false` means
*this control exists and did not run this time*, and there is no AML control here at all. The
truthful representation of a control an implementation lacks is the key's **absence**, which
`IMPLEMENTED_CONTROLS = ("trust", "risk", "roi")` enforces and
`test_a_control_this_implementation_lacks_is_absent_not_zero` asserts, with the reasoning already
written down: *"reporting `aml: {score: 0}` would claim a clean screening that never happened."*

**Absent is not not-run.** The four-states rule applies to the record's own vocabulary, and the
change was reverted.

**So the conclusion inverts, and the honest version is better.** The profile keeps the requirement,
and **tesoro does not conform to `stablecoin-1`** until a screening provider is integrated behind
the control. A profile is a bar; an implementation that has not cleared it declares which profile it
*does* meet — `aegs-2` — and says why. That is the same posture as publishing two open red-team
findings, and it is more useful to an obliged entity than a record that pretends to a control.

The satisfiable path is to build the control, not to widen the record: the `sanctions` control
already exists as the highest-precedence dispositive control, so a real provider has somewhere to
land.

Three further gaps, in order of how much they matter to this vertical:

| Gap | Status | Note |
|---|---|---|
| No AML control at all | **blocks conformance to `stablecoin-1`, correctly** | Not fixable by editing the record. Needs a provider behind the existing `sanctions` slot |
| No jurisdiction as a policy fact | open | The AML schema *already has* a `jurisdiction` field; nothing populates it, and nothing can rule on it |
| No Travel Rule originator/beneficiary fields | open | AEGS should define the **record**, never the transfer |
| Agent→human attribution not framed as *originator* attribution | open | The capability exists; the framing does not, and the framing is what makes it legible to a compliance team |

**What is already there** and should not be rebuilt: integer atomic units for six-decimal assets;
two channels that never share an envelope; irreversibility as the reason controls sit before the
payment; per-counterparty and per-resource envelopes; the delegation clamp; the evidence chain with
anchoring; and a `sanctions` control that is already the highest-precedence dispositive control —
so integrating a real screening provider has somewhere to land.

---

## 7 · What must not be claimed

Carried from [`claims-register.md`](claims-register.md) §3, because this vertical is where the
temptation is strongest and the cost of getting it wrong is highest.

- **Not compliance.** GENIUS obligations fall on Permitted Payment Stablecoin Issuers, MiCA's on
  EMT/ART issuers and CASPs, the Travel Rule's on VASPs. A library is none of those.
- **Not AML screening.** No list, no matching, no jurisdiction model.
- **Not a substitute for KYC/KYB.** The opposite: it consumes that signal.
- **Not Travel Rule compliance.** A record shape is not a transfer protocol.
- **Not "audited" or "independently validated."** Every conformance case and adversarial attack was
  written by the author of the system under test.

The guide models the honest posture, and it is worth copying its restraint: it states plainly that
it is *"provided for general information purposes"* and is not legal advice.

---

## 8 · Why this is worth sending to a compliance platform

Two audiences, both from the guide's own segmentation.

**A compliance platform** (Sumsub is the guide's publisher, and serves all six segments) has a
customer problem arriving: clients whose users deploy agents, generating flow their monitoring was
not calibrated for, with originator fields that name someone who pressed nothing. They will not
build an economic governance layer — it is not their product — and **the interface is a signal
exchange, not an integration**: they supply screening and identity, they consume attributed
evidence.

**A card issuer settling in stablecoins** — KAST is the guide's card-issuer segment at scale, 1M+
users and ~$5bn annualised — has the sharper version. A card program's KYC is on the human; the
*actor* may be software. Their checklist requires KYC at onboarding, sanctions and PEP screening,
and card-scheme rules. **None of it models an autonomous actor spending against a verified human's
balance.**

The pitch is one sentence and it is not a product pitch:

> When your customer's agent makes a payment, your Travel Rule record has an originator who did not
> press the button. Here is the evidence that closes that gap — and here is what we deliberately do
> not do.

---

## 9 · Confidence, and what is unverified

Marked per the rules in [`README.md`](README.md).

- `verified` — the guide's seven frameworks, six segments and checklists, read directly from the
  PDF; the GENIUS Act timeline, independently confirmed; x402 volumes from x402.org; KAST's
  segment, scale and funding; the missing `aml` key, measured from a live record.
- `recalled` — that FATF R.16's originator field has no representation for delegated or autonomous
  initiation. **Plausible and not confirmed against the R.16 text.** If some jurisdiction's
  implementation already carries such a field, §3(a) needs softening. **Check before sending
  anything to anyone.**
- `open` — whether any regulator has published guidance on agent-initiated transfers. Nothing found,
  nothing searched for properly.
- `open` — MiCA, FCA, MAS, HKMA and VARA specifics are as the guide states them, not independently
  verified.
