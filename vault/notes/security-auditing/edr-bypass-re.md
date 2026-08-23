---
title: edr-bypass-re
aliases:
  - edr bypass re
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/edr-bypass-re/SKILL.md
created: 2026-08-19
---

# edr-bypass-re

> [!info] What it does
> 逆向防御方实现 → 红队针对性绕过。把 EDR / Defender / AV 的 hook 表、ETW provider、AMSI 实现先逆向出来， 再写针对性的 unhook / 间接 syscall / ETW patch / call stack spoof。对照 MITRE ATT&CK T1562 防御规避。 触发关键词：EDR 绕过、AV bypass、免杀、unhook、direct syscall、indirect syscall、Hell's Gate、Halo's Gate、 Tartarus Gate、ETW patch、AMSI patch、call stack spoofing、hardware breakpoint Blindside、MITRE T1562、 ntdll unhook、kernel callback、CrowdStrike 绕过、Defender 绕过、Sentinel One 绕过、Elastic Defend、 Sysmon 规避、PPID spoof、Sleep mask、Process Hollowing、Reflective DLL。

**Source:** [skills/edr-bypass-re/SKILL.md](../../../skills/edr-bypass-re/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

_None auto-detected. Add your own links here, e.g. `[[scanpy]]`._

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
