# Architecture Ladder

```text
                         MORE CONTROLLED CAPABILITY
                                  ^
                                  |
Level 5   Multi-agent       roles + coordination + shared state
             ^
Level 4   Stateful agent   durable state / graph orchestration
             ^
Level 3   Agent            decision loop + tools + bounded actions
             ^
Level 2   RAG              runtime retrieval + grounded generation
             ^
Level 1   LLM app          prompt/context + model + validation
             ^
Level 0   Deterministic    rules / APIs / conventional software

                                  |
                                  v
                         MORE OPERATIONAL COMPLEXITY
```

**Important:** the vertical position is not a quality ranking. Choose the lowest level that satisfies requirements; move upward only when additional capability produces measurable value.
