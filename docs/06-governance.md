# 6. Governance: who pays, whose data

[Workshop home](../README.md) · Back: [5. Copilot Studio](05-copilot-studio.md)

## Who pays for what

| Part | Billed to |
|---|---|
| Fabric data agent (every question) | Your **Fabric capacity** (CUs) |
| Copilot Studio, standard harness | After publish: Copilot Credits, except licensed Microsoft 365 Copilot users running it as themselves |
| Copilot Studio, Microsoft Copilot harness | **Copilot Credits from the moment you build**, including testing |
| Foundry agent | Model tokens to your **Azure** subscription; the data agent still to Fabric |

## Whose data

- **User** authentication: each person sees only what they can already see. They need Read on the data agent and its sources. RLS and CLS still apply.
- **Maker** authentication: everyone sees what the builder can see. Convenient, and a data-exposure decision. Make it on purpose.
- Querying a semantic model through a data agent needs only **Read**. Prep for AI needs **Write**.

## Where the data goes

- If your capacity is outside the US or EU, prompts and results are processed in the EU Data Boundary or US, and your admin must allow **cross-geo processing and storing** for AI.
- Answers returned to Copilot Studio can leave the Fabric compliance boundary.

## Watch list

- **Q&A retirement (February 2027):** Prep for AI depends on Q&A today.
- **Build agent with AI:** preview, SQL and Eventhouse only.
