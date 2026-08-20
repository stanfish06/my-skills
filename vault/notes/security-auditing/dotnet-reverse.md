---
title: dotnet-reverse
aliases:
  - dotnet reverse
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/dotnet-reverse/SKILL.md
created: 2026-08-19
---

# dotnet-reverse

> [!info] What it does
> .NET / C# 二进制逆向。当目标是 .NET assembly（PE 头含 CLR、.exe/.dll 托管程序）、C# 编译产物（含 NativeAOT）、红队 Sharp* 工具（Rubeus / SharpHound / SharpHound 等）、.NET 混淆程序（ConfuserEx / SmartAssembly / Babel / Eazfuscator）、.NET loader / info-stealer / 套壳 malware 时使用。优先用 dnSpyEx + de4dot，需要 AI 直接操作时联动 dnSpy MCP。不用于纯 native 二进制（走 reverse-engineering / ida-reverse）。

**Source:** [skills/dotnet-reverse/SKILL.md](../../../skills/dotnet-reverse/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [ida-reverse](../../notes/security-auditing/ida-reverse.md) — IDA Pro 逆向分析辅助技能。当用户提到逆向、反编译、分析二进制/PE/ELF/APK/DLL/SO、破解、找密码、漏洞分析、病毒分析、firmware 固件分析，或需要分析 exe/dll/so/elf/macho/sys 等文件时，务必使用此技能。 Ensure to use this skill when the user wants to analyze...
- [reverse-engineering](../../notes/security-auditing/reverse-engineering.md) — Provides reverse engineering techniques

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
