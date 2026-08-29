<!--
  Design rules for this README (adopted 2026-08-30 after testing alternatives):
  - every visual is a self-generated SVG committed to generated/ — no third-party
    widget services (rejected: github-readme-stats' public instance rate-limits,
    a streak card would show ~0, typing-svg relies on SMIL which camo strips)
  - each panel ships as a dark/light <picture> pair; GitHub's camo proxy strips
    SMIL and external fonts, so animation is CSS keyframes only, inside the SVGs
  - projects are hand-picked in config.json ("projects"), never sorted by stars
  - if a panel's data source degrades, the build falls back to the committed
    caches in generated/ — the page goes stale, never broken
-->
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/dark_mode.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/light_mode.svg" />
  <img alt="Rudray Mehra — terminal-style profile with an ASCII portrait and live GitHub stats" width="1000" src="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/dark_mode.svg" />
</picture>

<br>

<sub>$ cat about.txt</sub>

<samp>Full-stack + AI/ML engineer at Scaler Innovation Labs, Bengaluru.<br>
I build servers from scratch, RAG pipelines, and AI agents that review code.<br>
TypeScript · Java · Python · Rust</samp>

<br>
<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/projects_dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/projects_light.svg" />
  <img alt="$ ls ~/projects — citepdf: citation-first PDF RAG with RAPTOR tree, contextual retrieval and hybrid Qdrant search (Python); http-server: production-style HTTP server from scratch with multi-threading and security controls (Java); ai-cli-agent: a Gemini agent on a strict think-tool-observe loop (TypeScript); reviewbot: a Claude-powered pull-request reviewer with an adversarial verify pass (Python); rudraymehra: this page, drawn from scratch into SVG daily (Python)" width="1000" src="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/projects_dark.svg" />
</picture>

<sub><a href="https://github.com/rudraymehra/citepdf">citepdf</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="https://github.com/rudraymehra/HTTP-SERVER">http-server</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="https://github.com/rudraymehra/AI-CLI-AGENT">ai-cli-agent</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="https://github.com/rudraymehra/reviewbot">reviewbot</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="scripts/">this profile</a></sub>

<br>
<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/activity_dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/activity_light.svg" />
  <img alt="$ ./activity.sh --last-year — a hand-drawn contribution heatmap for the past year beside top-language share bars, ending with a blinking terminal cursor" width="1000" src="https://raw.githubusercontent.com/rudraymehra/rudraymehra/main/generated/activity_dark.svg" />
</picture>

<br>

<sub>No templates, no third-party widgets — every window above is regenerated daily by <a href=".github/workflows/build.yml">GitHub Actions</a> from <a href="scripts/">original Python</a>: ASCII portrait, dot-leader stats, heatmap, and bars are all drawn from scratch into static SVG. <a href="docs/SETUP.md">Build your own →</a></sub>

<br>
<br>

<sub><code>$ exit</code>&nbsp;&nbsp;—&nbsp;&nbsp;Connection to rudray@github closed. Say hi: <a href="mailto:rudraymehra@gmail.com">rudraymehra@gmail.com</a></sub>

</div>
