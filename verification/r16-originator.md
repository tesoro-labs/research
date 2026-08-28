# Verification: does FATF R.16 represent delegated or autonomous initiation?

**Checked 2026-08-28 against primary sources.** This note exists because the claim was marked
`recalled` in [`../stablecoin-agents-gap.md`](../stablecoin-agents-gap.md) §9 and was load-bearing
for §3(a), and because that file said in as many words: *check before sending anything to anyone.*

## The claim as it was written

> Nothing in the Travel Rule payload distinguishes: a person who reviewed and sent this payment; a
> person who delegated authority to an agent that sent it under policy; a person whose credentials
> an agent used after being compromised.

## Verdict: the claim splits three ways

| Rail | Verdict |
|---|---|
| **FATF R.16 required data set** | **Confirmed.** No such element exists |
| **ISO 20022 fiat rails (CBPR+ pacs.008)** | **Refuted as worded.** An optional `InitgPty` exists |
| **IVMS101 — the stablecoin/VASP Travel Rule payload** | **Confirmed.** No such element exists |

The wording "the Travel Rule payload" was too broad. The corrected wording is narrower, and the
supporting evidence found while checking is *stronger* than what it replaces.

## Sources read

1. **FATF, *The FATF Recommendations*, 2012–2025** (152pp) — retrieved 2026-08-28 from
   `fatf-gafi.org/content/dam/fatf-gafi/recommendations/FATF Recommendations 2012.pdf`, 1,483,401
   bytes. This is the consolidated text *after* the June 2025 R.16 revision.
2. **FATF, *Explanatory note for revised R.16*** — same host, 987,485 bytes, 22pp. A redline
   document: it shows the June 2025 changes as struck and inserted text.
3. **Clearstream, *Usage Guideline CBPRPlus-pacs.008.001.08_FIToFICustomerCreditTransfer*** —
   the CBPR+ cross-border payment message as banks actually implement it.
4. **IVMS101** (interVASP Messaging Standard) — the data model VASPs use to satisfy R.16 for
   virtual-asset transfers.

Search of the FATF consolidated text, whole document:

| Term | Hits |
|---|---|
| `initiating party` | **0** |
| `ultimate debtor` | **0** |
| `artificial intelligence` | **0** |

## Finding 1 — the required data set has no initiator element

INR.16 ¶9, the set that must accompany a qualifying cross-border transfer above the threshold:

> (a) the name of the originator and beneficiary; (b) the account number of the originator and
> beneficiary where such an account is used to process the transaction \[…] In the absence of an
> account, a unique transaction reference number should be included \[…]; (c) the address of the
> originator \[…] and the country and town name (or the nearest alternative) of the beneficiary,
> \[…] (d) or where the originator is a natural person, national identity number, or customer
> identification number, or the date and place of birth of the originator; and (e) where the
> originator and/or beneficiary is a legal person \[…] the connected business identifier code
> (BIC) \[or LEI or unique official identifier].

Every element identifies **who the money belongs to**. None identifies **who instructed the
movement**, and none carries the *basis* on which it was instructed.

## Finding 2 — the 2025 revision moved *away* from delegated authority

This was not anticipated and it is the strongest thing in this note.

The FATF glossary definition of *originator* was changed in June 2025. The explanatory note's
redline reads, with the struck word still recoverable from the text layer:

> Originator refers to the account holder who ~~allows~~ **requests** the payment or value transfer
> from that account, or where there is no account, the natural or legal person that places the
> order with the ordering financial institution to perform the payment or value transfer.

The adopted text in the consolidated Recommendations confirms which side of the redline survived:

> Originator refers to the account holder who **requests** the payment or value transfer from that
> account \[…]

**"Allows" would have covered an account holder who authorised a standing policy.** "Requests" does
not. In 2025 the standard narrowed the definition to an act of requesting, at the exact moment
software began doing the requesting.

Two honest caveats. The revision's stated purpose is payment transparency and ISO 20022 alignment,
and nothing in the explanatory note suggests agents were considered — `artificial intelligence`
does not appear in the document. So this is a **consequence** of the change, not its intent, and
should be presented as one. And "requests" is arguably the more natural reading of what an account
holder does; the change tightens sloppy drafting rather than deliberately excluding delegation.

## Finding 3 — footnote 48 is the bridge to ISO 20022, and it lands on Debtor

INR.16 ¶4:

> Information accompanying cross-border and domestic payments or value transfers should be
> structured, to the extent possible, in accordance with the established standards of the system
> used such as ISO 20022, and should be sufficiently detailed to enable identification of the
> originator and beneficiary.

Footnote 48:

> The terms "originator" and "beneficiary" \[…] are interchangeable with the terms "debtor" and
> "creditor" respectively, which are used in certain messaging standards such as ISO 20022.

So R.16's *originator* maps to ISO 20022 **Debtor** — not to InitiatingParty and not to
UltimateDebtor. R.16 reaches into ISO 20022 and picks the party whose account is debited.

## Finding 4 — the refutation: fiat rails do carry an initiating party

The CBPR+ pacs.008 usage guideline contains, verbatim:

> `4  Initiating Party  <InitgPty>  [0..1]  Rules: R45`

at path
`Document/FIToFICustomerCreditTransferV08/CreditTransferTransactionInformation/InitiatingParty`,
and alongside it:

> `4  Ultimate Debtor  <UltmtDbtr>  [0..1]  Rules: R39, R40, R41, R42`

**So "nothing in the payload distinguishes" is false on fiat rails.** A structural place to say
"this payment was initiated by someone other than the debtor" exists and has existed for years.

Four things bound how much this costs the argument:

1. **`[0..1]` — optional, and not among R.16's required elements.** A field nobody must populate
   cannot be relied on by a receiving institution's monitoring.
2. **It names a party, not a mode.** The element carries `Name`, `PostalAddress`, `Identification`.
   It answers *who*, never *under what authority* or *when that authority was conferred*.
3. **An agent cannot be one.** `InitgPty` expects a legal or natural person. An agent has no legal
   personality — which is the same fact that keeps it outside all seven frameworks.
4. **It still does not separate the three cases.** Delegated-under-policy and
   compromised-credentials produce an identical `InitgPty`, or an absent one. That was always the
   sharp end of the claim, and it survives intact.

## Finding 5 — IVMS101, the rail this project targets, has nothing

The originator structure is `originatorPersons` (array of `Person`) plus `accountNumber`. Positions
after the first may hold `naturalPerson` representatives of a legal person — organisational
structure, not delegation of authority. There is **no initiating-party, on-behalf-of, agent, or
delegated-authority element.**

Since stablecoin transfers between VASPs are the rail in scope, the claim holds in full where it
matters most, and now holds for a checkable reason rather than a remembered one.

## What changed downstream

| File | Change |
|---|---|
| `stablecoin-agents-gap.md` §3(a) | Rewritten: scoped to the required set and IVMS101, `InitgPty` conceded, "allows"→"requests" added |
| `stablecoin-agents-gap.md` §9 | `recalled` row replaced by `verified`, pointing here |
| `report/body.html` §2.1, §7 | Same, and the confidence table's Recalled row is gone |
| `where-we-stand.svg` | Middle card of the assumptions band reworded |

## What is still not verified

- Whether any jurisdiction's *implementation* of R.16 adds an initiator field beyond the FATF
  minimum. Seven frameworks were not each read; the FATF text was.
- Whether any regulator has published guidance on agent-initiated transfers. Still `open`.
- The redline direction in Finding 2 is inferred from text-layer extraction of a struck word plus
  the adopted text of the consolidated Recommendations. Both readings agree, and the conclusion
  rests on the adopted text alone, which is unambiguous.
