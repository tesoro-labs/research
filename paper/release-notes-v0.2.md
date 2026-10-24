**Which control decided? Required attribution in pre-execution payment governance**, preprint draft v0.2.

Jayath de Silva ([ORCID 0009-0007-1855-4158](https://orcid.org/0009-0007-1855-4158)) · Independent

When controls can only make a payment verdict stricter, the order they run in never changes the verdict, but it does change which control the record names whenever two of them refuse. The paper argues that agent payment governance should require that record, and works out what requiring it costs.

New in v0.2:

- **Where should the control sit?** A map of six places a spending control can act on one x402 payment (pre-tool hook, client spend controls, custodial signer, agent gateway, seller, facilitator), what each can see, and four gaps none of them closes on its own: the price is the seller's word, budgets split across layers disagree, attribution has to name the layer, and a refusal in transit does not revoke a signature.
- Four figures and two comparison tables; prose rewritten for readability, claims unchanged.
- A correction: the twenty-attack benchmark score is in a test-checked baseline file, and the last sealed record covers eighteen attacks.

`paper.pdf` attached (21 pages). Not peer reviewed. Measured figures resolve to sealed records EXP-007 to EXP-010 in [`tesoro-labs/aegs`](https://github.com/tesoro-labs/aegs/tree/main/research/experiments) or to `redteam/baseline.json` in [`tesoro` 0.1.3](https://pypi.org/project/tesoro/0.1.3/); their limitations apply. Drafting and figures used an AI assistant; the author checked every claim and source.

Cite all versions: [10.5281/zenodo.23610076](https://doi.org/10.5281/zenodo.23610076). Licence: CC BY 4.0.
