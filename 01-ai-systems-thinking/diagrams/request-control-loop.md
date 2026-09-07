# Request Control Loop

```text
User request
    |
    v
[Authenticate]
    |
    v
[Validate input]
    |
    v
[Acquire approved context]
    |
    v
[Model / planner]
    |
    +-------------------------+
    |                         |
    v                         v
[Answer]                 [Tool request]
                              |
                              v
                      [Validate arguments]
                              |
                              v
                      [Authorize action]
                              |
                              v
                        [Execute tool]
                              |
                              v
                         [Observe]
                              |
                              +----> planner/model

All paths emit:
  trace_id | latency | errors | policy events | token/cost data
```
