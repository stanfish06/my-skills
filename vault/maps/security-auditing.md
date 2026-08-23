---
title: Security & Auditing
tags:
  - skill-map
created: 2026-06-13
---

# Security & Auditing

> [!abstract] Scope
> Secure development, code auditing, static analysis, SARIF, fuzzing, agent security, supply-chain risk, and smart-contract review helpers.

[Back to Skill Index](../index.md)

**Related maps:** [Cloud, Infra & MLOps](cloud-devops.md) | [Vault, Skills & Workflow Meta](vault-meta.md) | [Analytics Engineering & LLM Operations](analytics-engineering.md) | [Web Automation, Frontend & Design](web-automation-frontend.md) | [.NET & C# Development](dotnet-development.md)

## Skills (89)

- [aflpp](../notes/security-auditing/aflpp.md) — AFL++ is a fork of AFL with better fuzzing performance and advanced features
- [agentic-actions-auditor](../notes/security-auditing/agentic-actions-auditor.md) — Audits GitHub Actions workflows for security vulnerabilities in AI agent integrations including Claude Code Action, Gemini CLI, OpenAI Codex, and GitHub AI Inference
- [api-security](../notes/security-auditing/api-security.md) — Use for authorized security assessment of REST, GraphQL, WebSocket, or SOAP APIs, including discovery, authentication, authorization, rate-limit, and CI/CD testing
- [apk-reverse](../notes/security-auditing/apk-reverse.md) — 在 CLI 环境下做 Android APK 逆向时使用。适用于 APK 解包、Java 反编译、smali 修改、重打包、Frida 动态 Hook，以及按需切换到 so/native 分析。优先使用本机已安装的 jadx、apktool、frida、adb、ida-reverse、radare2。
- [atheris](../notes/security-auditing/atheris.md) — Atheris is a coverage-guided Python fuzzer based on libFuzzer
- [attack-chain](../notes/security-auditing/attack-chain.md) — Use for authorized multi-stage attack-path planning and orchestration when a task spans reconnaissance, initial access, privilege escalation, lateral movement, or impact assessment
- [attack-path-analysis](../notes/security-auditing/attack-path-analysis.md) — Use when Codex is already in the attack-path-analysis phase of a security scan or the user explicitly asks to trace a security finding from source to sink and calibrate severity
- [audit-and-reduce-dependencies](../notes/security-auditing/audit-and-reduce-dependencies.md) — Reduces JavaScript dependency footprint with pnpm while preserving lockfile, workspace layout, and dependency range style
- [audit-context-building](../notes/security-auditing/audit-context-building.md) — Understand a codebase before looking for bugs in it - what each function assumes, what it guarantees, and what it depends on elsewhere
- [audit-prep-assistant](../notes/security-auditing/audit-prep-assistant.md) — Prepares codebases for security review using Trail of Bits' checklist
- [auth](../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [binary-diff](../notes/security-auditing/binary-diff.md) — 跨版本符号迁移与二进制差分。当你有旧版本的符号/逆向结果，需要快速迁移到新版本时使用。 适用场景：内核缺 PDB 用旧版符号推导、程序更新后批量迁移函数名、应用更新后快速定位新偏移。 核心方法：用 LLM 做结构化差异比对，程序化输入输出，成本极低（200 函数 ~1 元）。 触发关键词：符号迁移、bindiff、跨版本、PDB 缺失、函数偏移迁移、symbol...
- [browser-automation](../notes/security-auditing/browser-automation.md) — 统一自动化入口。覆盖浏览器自动化（Playwright）和 Windows 桌面应用自动化（OpenReverse）。 浏览器场景：打开网页、点击、填表、爬取、截图、自动化登录、渗透页面交互。 桌面场景：操作 IDA/x64dbg 等 GUI 工具、Windows UI Automation、视觉驱动交互、桌面应用网络抓包。...
- [browser-extension-reverse](../notes/security-auditing/browser-extension-reverse.md) — Use for authorized reverse engineering of browser extensions (Chrome/Firefox) including manifest analysis, background workers, and extension-based credential or traffic logic recovery
- [c-review](../notes/security-auditing/c-review.md) — Performs comprehensive C/C++ security review for memory corruption, integer overflows, race conditions, and platform-specific vulnerabilities
- [cargo-fuzz](../notes/security-auditing/cargo-fuzz.md) — cargo-fuzz is the de facto fuzzing tool for Rust projects using Cargo
- [case-review](../notes/security-auditing/case-review.md) — Reviews a reverse-skill case package for scope readiness, Evidence to Finding to Path traceability, work item coverage, timeline references, and optional artifact hash integrity before...
- [check-npm](../notes/security-auditing/check-npm.md) — Audit a JavaScript/TypeScript repo's npm, yarn, or pnpm configuration for supply-chain hardening: tool version, lifecycle scripts, unsafe dependency protocols, and minimum release age...
- [cloud-k8s](../notes/security-auditing/cloud-k8s.md) — Use for authorized cloud, container, and Kubernetes security assessment including metadata SSRF, IAM misconfig, container escape paths, and cluster RBAC review
- [code-audit](../notes/security-auditing/code-audit.md) — Use for authorized source-code security review and SAST workflows including Semgrep, CodeQL patterns, dangerous API hunting, and fix verification
- [code-maturity-assessor](../notes/security-auditing/code-maturity-assessor.md) — Systematic code maturity assessment using Trail of Bits' 9-category framework
- [codeql](../notes/security-auditing/codeql.md) — Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis
- [constant-time-analysis](../notes/security-auditing/constant-time-analysis.md) — Detects timing side-channel vulnerabilities in cryptographic code
- [constant-time-testing](../notes/security-auditing/constant-time-testing.md) — Constant-time testing detects timing side channels in cryptographic code
- [coverage-analysis](../notes/security-auditing/coverage-analysis.md) — Coverage analysis measures code exercised during fuzzing
- [database-security](../notes/security-auditing/database-security.md) — Use for authorized database security assessment covering PostgreSQL/MySQL/MSSQL/Mongo/Redis exposure, authz, UDF/command paths, and misconfiguration review
- [deep-security-scan](../notes/security-auditing/deep-security-scan.md) — Use when the user asks for a deep, exhaustive, multi-pass, or variance-reducing repository-wide or scoped-path Codex Security scan
- [differential-review](../notes/security-auditing/differential-review.md) — Performs security-focused differential review of code changes (PRs, commits, diffs)
- [digital-forensics](../notes/security-auditing/digital-forensics.md) — Use for authorized digital forensics including memory dumps, disk timelines, PCAP investigation, artifact triage, and IR evidence preservation
- [dotnet-reverse](../notes/security-auditing/dotnet-reverse.md) — .NET / C# 二进制逆向。当目标是 .NET assembly（PE 头含 CLR、.exe/.dll 托管程序）、C# 编译产物（含 NativeAOT）、红队 Sharp* 工具（Rubeus / SharpHound / SharpHound 等）、.NET 混淆程序（ConfuserEx / SmartAssembly / Babel /...
- [edr-bypass-re](../notes/security-auditing/edr-bypass-re.md) — 逆向防御方实现 → 红队针对性绕过。把 EDR / Defender / AV 的 hook 表、ETW provider、AMSI 实现先逆向出来， 再写针对性的 unhook / 间接 syscall / ETW patch / call stack spoof。对照 MITRE ATT&CK T1562 防御规避。 触发关键词：EDR 绕过、AV...
- [email-security](../notes/security-auditing/email-security.md) — Use for authorized email security review including phishing analysis, header authentication (SPF/DKIM/DMARC), BEC patterns, and mailbox token abuse research
- [entry-point-analyzer](../notes/security-auditing/entry-point-analyzer.md) — Analyzes smart contract codebases to identify state-changing entry points for security auditing
- [finding-discovery](../notes/security-auditing/finding-discovery.md) — Use when Codex is already in the finding-discovery phase of a security scan or the user explicitly asks to discover candidate security findings in a repository or code change
- [firmware-pentest](../notes/security-auditing/firmware-pentest.md) — 固件 / IoT 渗透链。从拿到一坨 .bin / .img 开始，闭环走完逆向 → 提取 → 模拟 → 利用。 方法论遵循 OWASP FSTM 九阶段；工具链以 binwalk v3、unblob、EMBA、Firmadyne、AFL++ 为主。 适用场景：路由器/摄像头/智能家居固件审计、固件升级包逆向、IoT CVE 复现、嵌入式 0day 挖掘。...
- [fix-finding](../notes/security-auditing/fix-finding.md) — Use when the user explicitly asks to fix and verify a validated or plausible security finding
- [fp-check](../notes/security-auditing/fp-check.md) — Systematically verifies suspected security bugs to eliminate false positives, producing a TRUE POSITIVE or FALSE POSITIVE verdict with documented evidence for each
- [fuzzing-dictionary](../notes/security-auditing/fuzzing-dictionary.md) — Fuzzing dictionaries guide fuzzers with domain-specific tokens
- [fuzzing-obstacles](../notes/security-auditing/fuzzing-obstacles.md) — Techniques for patching code to overcome fuzzing obstacles
- [gh-cli](../notes/security-auditing/gh-cli.md) — Enforces authenticated gh CLI workflows over unauthenticated curl/WebFetch patterns
- [ghidra-reverse](../notes/security-auditing/ghidra-reverse.md) — Use for free/open reverse engineering with Ghidra (headless or GUI), including decompile, cross-refs, and optional Ghidra MCP workflows when IDA is unavailable
- [go-rust-reverse](../notes/security-auditing/go-rust-reverse.md) — Use for reverse engineering stripped Go and Rust binaries including runtime recognition, pclntab/moduel data recovery, panic strings, and idiomatic decompilation recovery
- [guidelines-advisor](../notes/security-auditing/guidelines-advisor.md) — Smart contract development advisor based on Trail of Bits' best practices
- [hardware-security](../notes/security-auditing/hardware-security.md) — Use for authorized hardware and embedded interface security research including UART/JTAG discovery, debug pad triage, secure boot overview, and offline firmware extraction support
- [harness-writing](../notes/security-auditing/harness-writing.md) — Techniques for writing effective fuzzing harnesses across languages
- [ida-reverse](../notes/security-auditing/ida-reverse.md) — IDA Pro 逆向分析辅助技能。当用户提到逆向、反编译、分析二进制/PE/ELF/APK/DLL/SO、破解、找密码、漏洞分析、病毒分析、firmware 固件分析，或需要分析 exe/dll/so/elf/macho/sys 等文件时，务必使用此技能。 Ensure to use this skill when the user wants to analyze...
- [identity-federation](../notes/security-auditing/identity-federation.md) — Use for authorized assessment of federated identity systems including SAML, OIDC, OAuth2 flows, SSO misconfiguration, and token confusion issues
- [insecure-defaults](../notes/security-auditing/insecure-defaults.md) — Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production
- [js-reverse](../notes/security-auditing/js-reverse.md) — 在使用 js-reverse-mcp 做前端 JavaScript 逆向时使用，适用于签名链路定位、页面观察取证、运行时采样、本地补环境复现与证据化输出。优先适配当前环境里的 js-reverse_* 工具，需要更强的浏览器/CDP/Hook 面时联动 jshookmcp。
- [libfuzzer](../notes/security-auditing/libfuzzer.md) — Coverage-guided fuzzer built into LLVM for C/C++ projects
- [llm-agent-security-redteam](../notes/security-auditing/llm-agent-security-redteam.md) — LLM and agent security red teaming with agentic-actions-auditor, supply-chain-risk-auditor, semgrep, codeql, and sarif-parsing
- [llm-security](../notes/security-auditing/llm-security.md) — Use for authorized security assessment of LLM applications and AI agents, including prompt injection, tool abuse, RAG exposure, memory poisoning, and model supply-chain risks
- [macos-reverse](../notes/security-auditing/macos-reverse.md) — Use for authorized macOS and Mach-O reverse engineering including codesign, Objective-C/Swift recovery, endpoint security surfaces, and Apple platform malware analysis
- [malware-analysis](../notes/security-auditing/malware-analysis.md) — Use when analyzing suspected malware through static, dynamic, and behavioral techniques, including IOC extraction, YARA or Sigma rules, sandboxing, and anti-analysis behavior
- [mobile-reverse](../notes/security-auditing/mobile-reverse.md) — Use for authorized Android or iOS application reverse engineering and security testing, including APK or IPA analysis, runtime instrumentation, SSL pinning, and platform protection...
- [ossfuzz](../notes/security-auditing/ossfuzz.md) — OSS-Fuzz provides free continuous fuzzing for open source projects
- [ot-ics](../notes/security-auditing/ot-ics.md) — Use for authorized OT/ICS security assessment covering Purdue model zoning, PLC/SCADA exposure, industrial protocol discovery, and safe passive-first evaluation
- [patch-diff-exploit](../notes/security-auditing/patch-diff-exploit.md) — N-day 补丁差分到利用。从厂商发布的补丁里反推漏洞点、写 PoC、做成可用的攻击模块。 适用场景：已知 CVE 编号但只有补丁没有 PoC、SRC/红队需要打击未及时更新的资产、N-day 武器化、Patch Tuesday 跟进。 核心方法：拿 before/after 二进制 → 对齐符号 → 二进制 diff → 看新增的安全检查反推 bug class...
- [pentest-tools](../notes/security-auditing/pentest-tools.md) — 主动渗透测试工具链。覆盖信息收集、端口扫描、漏洞扫描、Web 渗透、SQL 注入、目录爆破、密码破解等场景。 通过 MCP server（pentestMCP / mcp-security-hub）将 20+ 安全工具暴露给 AI agent。 触发关键词：渗透测试、端口扫描、Nmap、漏洞扫描、Nuclei、SQL...
- [property-based-testing](../notes/security-auditing/property-based-testing.md) — Writes, reviews, and debugs property-based tests — Hypothesis, fast-check, proptest, jqwik, rapid, and Echidna or Medusa for Solidity invariants
- [propose-security-hardening](../notes/security-auditing/propose-security-hardening.md) — Develop evidence-backed structural and architectural security hardening proposals from vulnerability disclosures, supplied findings, incident or assessment documents, source code, or a...
- [protocol-reverse](../notes/security-auditing/protocol-reverse.md) — Use for authorized reverse engineering of custom binary protocols, Protobuf/gRPC, WebSocket frames, and PCAP-driven protocol recovery
- [pwn-chain](../notes/security-auditing/pwn-chain.md) — 从逆向走到可用利用 (Working Exploit) 的全链路工程化方法。 适用场景：拿到了二进制 + 漏洞点 + 目标环境，需要写出一个能稳定打通的 exploit（不是只能本地复现一下、远程一打就崩的脚本）。 覆盖三大方向：栈溢出 / 堆利用 / 内核 pwn。强调"CTF 本地通 → 真实远程稳定打通"的工程差距：libc...
- [radare2](../notes/security-auditing/radare2.md) — Use this skill whenever the user wants to analyze binaries with radare2/r2 from the command line, including reverse engineering, disassembly, function analysis, strings/import...
- [radio-sdr](../notes/security-auditing/radio-sdr.md) — Use for authorized RF/SDR security research including signal identification, replay feasibility study in shielded labs, and wireless protocol analysis outside classic Wi-Fi
- [reverse-engineering](../notes/security-auditing/reverse-engineering.md) — Provides reverse engineering techniques
- [reverse-skill-router](../notes/security-auditing/reverse-skill-router.md) — Routes reverse engineering, exploitation, penetration testing, malware, mobile, firmware, browser automation, documentation, and security tasks to the appropriate specialist skill
- [sarif-parsing](../notes/security-auditing/sarif-parsing.md) — Parses and processes SARIF files from static analysis tools like CodeQL, Semgrep, or other scanners
- [secure-workflow-guide](../notes/security-auditing/secure-workflow-guide.md) — Guides through Trail of Bits' 5-step secure development workflow
- [security-and-hardening](../notes/security-auditing/security-and-hardening.md) — Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations
- [security-diff-scan](../notes/security-auditing/security-diff-scan.md) — Use when the user asks for a security review of a pull request, commit, branch diff, working-tree patch, or other Git-backed change set
- [security-scan](../notes/security-auditing/security-scan.md) — Use for a standard, single-pass security audit of an entire repository or a scoped path, package folder, or submodule with no diff to review
- [semgrep](../notes/security-auditing/semgrep.md) — Runs a Semgrep security scan over a codebase: detects languages, selects rulesets, presents the plan for explicit approval, then runs every approved ruleset through...
- [semgrep-rule-creator](../notes/security-auditing/semgrep-rule-creator.md) — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns
- [sharp-edges](../notes/security-auditing/sharp-edges.md) — Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes
- [spec-to-code-compliance](../notes/security-auditing/spec-to-code-compliance.md) — Check code against the documentation that specifies it - which requirements hold, which the code contradicts, which are absent, and what the code does that no document mentions
- [supply-chain-risk-auditor](../notes/security-auditing/supply-chain-risk-auditor.md) — Audits a project's dependencies for supply-chain risk: version-matched advisories for direct dependencies and the full lockfile tree, abandoned or archived upstreams, npm publisher...
- [supply-chain-security](../notes/security-auditing/supply-chain-security.md) — Use for software supply-chain security assessment covering SBOM, SCA, CI/CD pipelines, container images, build integrity, dependency provenance, and vulnerability reachability
- [thick-client](../notes/security-auditing/thick-client.md) — Use for authorized security testing of desktop thick clients including local storage, update channels, IPC, traffic, and client-side trust boundaries
- [threat-hunting](../notes/security-auditing/threat-hunting.md) — Use for blue-team threat hunting, detection engineering with Sigma/YARA, SIEM query design, and incident detection validation
- [threat-model](../notes/security-auditing/threat-model.md) — Use when Codex is already in the threat-modeling phase of a security scan, the user explicitly invokes $threat-model, or the user explicitly asks to create, update, or persist a...
- [token-integration-analyzer](../notes/security-auditing/token-integration-analyzer.md) — Token integration and implementation analyzer based on Trail of Bits' token integration checklist
- [track-findings](../notes/security-auditing/track-findings.md) — Track validated Codex Security findings in Linear, Jira, GitHub issues, or draft GitHub security advisories
- [triage-finding](../notes/security-auditing/triage-finding.md) — Use when the user supplies or imports existing security findings, vulnerability reports, or security/vulnerability Jira/Linear tickets from scanners, advisories, GitHub, Atlassian...
- [variant-analysis](../notes/security-auditing/variant-analysis.md) — Hunts for the other instances of a bug already found — the variants of one root cause across a codebase
- [vulnerability-writeup](../notes/security-auditing/vulnerability-writeup.md) — Write up vulnerabilities from disclosure documents, rough notes, supplied findings, PoCs, source code, or Codex Security scan output into polished, self-contained, source-backed reports
- [wifi-wireless](../notes/security-auditing/wifi-wireless.md) — Use for authorized wireless security assessment including Wi-Fi capture, WPA handshake analysis, rogue AP detection research, and lab-only deauth testing
- [windows-ad](../notes/security-auditing/windows-ad.md) — Use for authorized Active Directory and Windows identity attacks including Kerberos, AD CS, BloodHound paths, NTLM relay, and domain privilege escalation research
- [zeroize-audit](../notes/security-auditing/zeroize-audit.md) — Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with assembly-level analysis, and control-flow verification
