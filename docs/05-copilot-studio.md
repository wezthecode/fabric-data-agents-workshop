# 5. Expose it through Copilot Studio

[Workshop home](../README.md) · Back: [4. Test and tune](04-test-and-tune.md) · Next: [6. Governance](06-governance.md)

Copilot Studio and Foundry only see the **published** version of a data agent. There are three routes; pick the one your licences allow.

| Route | Where | Needs |
|---|---|---|
| **A. Connected agent** on the standard harness | Copilot Studio → your agent → **Agents → + Add → Microsoft Fabric** | Copilot Studio access. Billing starts after you publish; for a licensed Microsoft 365 Copilot user running it as themselves in Teams or Copilot Chat, generative answers and actions aren't charged |
| **B. Fabric IQ Data MCP tool** on the Microsoft Copilot harness | Copilot Studio → **Add a tool → Fabric IQ Data MCP** → pick the agent from the OneLake catalog | **Copilot Credits from the moment you start building**. Lets you choose **User** or **Maker** authentication |
| **C. Fabric IQ tool in Foundry** (preview) | Foundry → agent → **Tools → Add → Browse all tools → Fabric IQ (OneLake Catalog)** | A Foundry project; model tokens bill to Azure, the data agent's work to your Fabric capacity. Runs on behalf of the signed-in user |

All routes need Fabric and Copilot Studio (or Foundry) in the **same tenant**.

## Route A step by step

1. copilotstudio.microsoft.com → pick an environment → **Create → + New agent**. Name, description, save.
2. **Agents → + Add → Microsoft Fabric**. Create the connection, select `da_contoso_semantic`.
3. Ask question 1 in the test pane.
4. **Publish** to Teams and Microsoft 365, ask again from Teams, then check the agent's **Monitor** page for billed usage.

## ✅ Checkpoint 5

The same answer to question 1 in Fabric, in the Copilot Studio test pane, and in Teams.
