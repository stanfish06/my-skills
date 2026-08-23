---
title: pwn-chain
aliases:
  - pwn chain
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/pwn-chain/SKILL.md
created: 2026-08-19
---

# pwn-chain

> [!info] What it does
> 从逆向走到可用利用 (Working Exploit) 的全链路工程化方法。 适用场景：拿到了二进制 + 漏洞点 + 目标环境，需要写出一个能稳定打通的 exploit（不是只能本地复现一下、远程一打就崩的脚本）。 覆盖三大方向：栈溢出 / 堆利用 / 内核 pwn。强调"CTF 本地通 → 真实远程稳定打通"的工程差距：libc 版本错配、堆喷射时序、SMEP/SMAP/KASLR、栈对齐、远程缓冲。 核心工具链：pwntools + GEF/pwndbg + ROPgadget/Ropper + one_gadget + libc-database + qemu-system 内核调试。 触发关键词：pwn、栈溢出、堆溢出、ROP、ret2libc、ret2csu、one_gadget、libc-database、堆利用、tcache、fastbin、unsorted bin、kernel pwn、kROP、SMEP、SMAP、KASLR、modprobe_path、pwntools、GEF、pwndbg。

**Source:** [skills/pwn-chain/SKILL.md](../../../skills/pwn-chain/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

_None auto-detected. Add your own links here, e.g. `[[scanpy]]`._

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
