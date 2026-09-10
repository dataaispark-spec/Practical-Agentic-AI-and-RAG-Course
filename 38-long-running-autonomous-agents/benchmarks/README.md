# Module 38 Benchmark Contract

Compare checkpoint-per-step, checkpoint-per-N and event-log recovery on identical workloads.

Track: resume success, lost work, duplicate effects, recovery time, checkpoint overhead, queue backlog, p95 latency, cost/run and SLA compliance.

Required chaos cases: crash-before-effect, crash-after-effect, lease loss, provider outage, stale checkpoint, expired approval and budget exhaustion.

A result is incomplete without reproducible seeds, workload definition and recovery evidence.