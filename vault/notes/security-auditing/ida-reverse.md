---
title: ida-reverse
aliases:
  - ida reverse
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/ida-reverse/SKILL.md
created: 2026-08-19
---

# ida-reverse

> [!info] What it does
> IDA Pro 逆向分析辅助技能。当用户提到逆向、反编译、分析二进制/PE/ELF/APK/DLL/SO、破解、找密码、漏洞分析、病毒分析、firmware 固件分析，或需要分析 exe/dll/so/elf/macho/sys 等文件时，务必使用此技能。 Ensure to use this skill when the user wants to analyze any binary file, regardless of whether they explicitly mention "IDA" or "reverse engineering". This includes requests like "看看这个exe", "分析这个dll", "帮我破解", "找一下密码", "这个软件怎么注册", etc. Use the bundled scripts (scripts/start.ps1, scripts/open.ps1) for deterministic server management and file opening — do NOT write ad-hoc PowerShell commands for these operations.

**Source:** [skills/ida-reverse/SKILL.md](../../../skills/ida-reverse/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [apk-reverse](../../notes/security-auditing/apk-reverse.md) — 在 CLI 环境下做 Android APK 逆向时使用。适用于 APK 解包、Java 反编译、smali 修改、重打包、Frida 动态 Hook，以及按需切换到 so/native 分析。优先使用本机已安装的 jadx、apktool、frida、adb、ida-reverse、radare2。
- [dotnet-reverse](../../notes/security-auditing/dotnet-reverse.md) — .NET / C# 二进制逆向。当目标是 .NET assembly（PE 头含 CLR、.exe/.dll 托管程序）、C# 编译产物（含 NativeAOT）、红队 Sharp* 工具（Rubeus / SharpHound / SharpHound 等）、.NET 混淆程序（ConfuserEx / SmartAssembly / Babel /...
- [start](../../notes/vault-meta/start.md) — Use when starting Zoom work

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
