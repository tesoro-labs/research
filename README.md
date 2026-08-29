# research

Research artefacts for the white paper on autonomous economic governance, and for the standards
proposal that may follow it.

**This repository holds reasoning, not measurements.** Measurements live in
[`aegs/research/experiments`](https://github.com/tesoro-labs/aegs/tree/main/research) as sealed records
with checksums — EXP-007 through EXP-010 — and nothing here restates their numbers. A claim in this
repository either cites a sealed record or is marked unsupported.

| Artefact | What it is for |
|---|---|
| [`prior-art.md`](prior-art.md) | The novelty test, done properly. Every claim of originality checked against what already exists, with confidence marked per item |
| [`claims-register.md`](claims-register.md) | Every claim the paper intends to make, the specific evidence for it, and the claims that **cannot** be supported |
| [`paper/outline.md`](paper/outline.md) | Structure, contribution statement, and the argument order |
| [`paper/draft.md`](paper/draft.md) | The paper itself. §1–§4 drafted; §5–§10 outstanding |
| [`stablecoin-agents-gap.md`](stablecoin-agents-gap.md) | The gap analysis: seven frameworks, six obliged entities, and the actor none of them name |
| [`outreach/`](outreach/) | Two briefs for the two audiences the gap analysis identifies, with the rules that keep them honest and the objections they will meet. Drafts to adapt, never to send verbatim |
| [`verification/`](verification/) | One file per claim checked against a primary source, including the checks that **refuted** what was written. Cited from wherever the claim is made |
| [`report/`](report/) | The standing report — `body.html` and `report.css` are the editable parts, `build.py` assembles and renders, `where-we-stand.pdf` is the output |

**Some documents referenced here are internal and deliberately unpublished** — the workspace plan,
the context document, the upstream engagement plan and the business analysis. They are named without
links because a link that 404s is worse than a plain reference. Everything a reader needs to check a
claim in *this* repository is either here or in a sealed record in `aegs/research`.

---

## On sequencing: the white paper and the x402 proposal should be loosely coupled, in that order

The question was whether the paper should be driven by AEGL, AEGS **and** the x402 proposal
together. **Two refinements, and one of them is a disagreement.**

### They have different readers and opposite virtues

A **white paper** is judged on whether its contribution is defensible: it wants context, related
work, limitations, and a claim that survives an aggressive reviewer. A **protocol proposal** is
judged on whether a maintainer can adopt it on a Tuesday: it wants to be minimal, scoped, and
obviously not a land grab.

Optimising one damages the other. A proposal carrying a paper's worth of justification reads as
scope creep. A paper written as a proposal reads as vendor advocacy. **Write both, keep them
separate, and let the proposal cite the paper rather than contain it.**

### The order is already recorded, and it is not proposal-first

The upstream engagement plan (`UPSTREAM-x402.md`, internal) says it plainly at U3:

> Before any standards-shaped proposal. **A stranger proposing a framework gets closed; a stranger
> who fixed three real things gets read.**

Three findings from that research constrain the proposal and none of them has changed:

- **F2 — upstream explicitly declares this scope out of scope.** Excellent news for a
  *complementary* layer, and it means a proposal to add governance to x402 **core** should be
  declined, correctly. Any proposal has to be an extension or profile. F1 identifies
  `specs/extensions/` as the insertion point.
- **F3 — upstream already ships thin spend controls.** So the proposal is not "here is a thing you
  lack." It is "here is the part that gets hard, and here is what it costs to get right."
- **F4 — a maintainer has already flagged float precision in money conversion.** That is
  `AEGS-0.1-ARITH-1`'s exact subject, and there are vectors for it. **A small, genuinely useful
  contribution in precisely the area a later proposal will cover** is the best possible opening,
  and it is U3.1.

**Recommended order:** paper (standalone) → U3 contributions in parallel, starting with the float
issue → proposal last, minimal, as an extension, citing the paper.

The one thing that would change this: if upstream opens a governance-shaped discussion on its own,
the window matters more than the standing, and the order inverts.

### On what the paper should claim

Grounding it in AEGL and AEGS is right — they are the artefacts. But **they are the vehicle, not
the contribution.** A paper whose claim is *"we defined a layer and a standard"* invites the
obvious response: so did Microsoft, and so did OASIS in 2003.

The contribution that survives [`prior-art.md`](prior-art.md) is narrower and stronger:

1. **A reproducible adversarial benchmark** for pre-execution economic governance, with sealed
   provenance including a superseded record where a measurement was wrong.
2. **Attribution as a normative, conformance-scored property** — and see `prior-art.md`, because
   the honest version of this claim is *much* narrower than it first appears.
3. **"Bounded, not eliminated"** as the honest unit of a governance promise.

AEGL and AEGS are how those three are delivered.

---

## Working rules

Carried from the workspace context document (internal), because a research repository is where
they matter most.

1. **A number without a sealed record is not evidence.** Cite EXP-NNN or mark it unsupported.
2. **Prior art is cited before it is pointed out.** The novelty claim is only as strong as the
   survey behind it, and conceding the surface is what makes the narrow claim credible.
3. **Confidence is marked, per claim.** `verified` means a primary source was read this session.
   `recalled` means it comes from training and needs checking before publication. The distinction
   is the difference between a paper and an embarrassment.
4. **A limitation discovered late is promoted, not buried.** Every sealed record in `aegs/research`
   carries its own limitations section; the paper inherits all of them.
