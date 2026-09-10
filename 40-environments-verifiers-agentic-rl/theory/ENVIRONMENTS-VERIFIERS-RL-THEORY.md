# Module 40 — Environments, Verifiers & Agentic RL: Theory

## Environment as an engineering contract
An environment defines state, observations, legal actions, transition semantics, termination, reset, seed and artifacts. A prompt alone is not an environment because it does not provide a reliable executable definition of success.

## Verifier hierarchy
1. deterministic invariant;
2. state comparison;
3. domain rule engine;
4. independent model-assisted judge;
5. human adjudication for ambiguous/high-impact cases.

Use multiple verifiers when one can be gamed. Track false accepts and false rejects.

## Reward is not truth
A reward is an optimization signal. If it omits an important constraint, an agent may maximize reward while violating the real objective. Teach reward hacking by constructing deliberately weak rewards and then strengthening them with independent checks.

## Reproducibility
Every trajectory should carry task ID, environment version, seed, policy/model version, tool versions and verifier version. Reset must produce a known initial state.

## Offline/online boundary
Offline evaluation protects against uncontrolled feedback loops; online evaluation measures real behavior but can expose users or production systems to unsafe experimentation. Keep training, evaluation and production credentials and data boundaries explicit.

## RL-oriented lifecycle
`TASK → RESET → ACT → OBSERVE → VERIFY → SCORE → STORE → EVALUATE → IMPROVE`.

## Security invariants
Evaluation artifacts cannot be rewritten by the candidate; candidates cannot modify the external verifier; sandbox escapes fail closed; held-out tasks remain inaccessible to optimization.

## Exercises
Construct a reward that can be gamed, exploit it, then add a verifier that closes the exploit; compute a verifier confusion matrix; compare deterministic and model-assisted judges; design a held-out benchmark resistant to training contamination.
