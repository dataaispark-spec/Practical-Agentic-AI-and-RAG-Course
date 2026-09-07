# Module 1 — Interview Question Bank

## Conceptual

1. Why is an LLM not a database?
2. What is the core problem RAG solves?
3. What problem does an agent solve that plain RAG does not?
4. When would a deterministic workflow be better than an agent?
5. Why can multi-agent systems be worse than single-agent systems?
6. What makes an AI system production-ready rather than demo-ready?
7. Why should requirements precede framework selection?
8. What is an architecture decision record?
9. Why must an AI system have explicit output contracts?
10. What is the difference between a model capability and a system capability?

## Design

11. Design a private-knowledge assistant for a company with tenant isolation.
12. Add a read-only order-status API to the assistant.
13. Add a high-risk action and explain the approval boundary.
14. Explain where authentication, authorization, retrieval and tool checks occur.
15. Define quality, latency, reliability and cost objectives for the design.

## Debugging

16. Retrieval looks relevant but final answers are wrong. What do you inspect?
17. Task success stayed flat while cost tripled. What changed might explain it?
18. p95 latency doubled after adding an agent loop. How do you localize the increase?
19. Users report answers from old policies. What evidence would you collect first?
20. A correct answer is returned to an unauthorized user. Why is retrieval quality irrelevant to that security failure?

## Senior/Architect

21. Prove or disprove that your multi-agent design is worth its complexity.
22. How would you benchmark RAG against long-context prompting?
23. How would you build a model fallback strategy without silently changing product behavior?
24. How would you version prompts, retrieval configuration and evaluation datasets?
25. How would you design for a model provider outage?
26. How would you prevent an agent from becoming an authorization layer?
27. How would you design observability so an incident can be reconstructed?
28. How would you handle stale or conflicting source documents?
29. How would you choose between one large model call and several smaller calls?
30. What evidence would convince you to simplify the architecture?

## Behavioral / communication

31. Describe an AI design decision you would reverse after seeing production data.
32. Tell an interviewer about a failure caused by an incorrect assumption.
33. Explain a complex AI architecture to a non-technical stakeholder.
34. Defend a decision to *not* use an agent.
35. Defend a decision to add a human approval step.
