# RAG vs Agent

```text
Question
  |
  +-------------------------------+
  |                               |
  v                               v
Need external/current         Need to take an action
knowledge?                    or choose among tools?
  |                               |
  +-- No --> LLM app             +-- No --> RAG / LLM app
  |
  +-- Yes --> retrieve evidence  +-- Yes --> Agent / Workflow
                    |                           |
                    v                           v
               Ground answer             Plan -> validate
                                                -> authorize
                                                -> execute
                                                -> observe
```

RAG and agents are complementary concepts. RAG primarily addresses knowledge grounding; agents/workflows primarily address controlled decisions and actions.
