# 3. Build the agent, two ways

[Workshop home](../README.md) · Back: [2. Prep for AI](02-prep-for-ai.md) · Next: [4. Test and tune](04-test-and-tune.md)

## Agent 1: hand-built on the semantic model

1. **+ New item → Fabric data agent**, name `da_contoso_semantic`.
2. In the OneLake catalog, pick `sm_contoso_cycles` → **Add**. Tick all six tables in the Explorer.
3. Leave **Agent instructions** empty for now.

## Agent 2: built with AI on the warehouse

1. **+ New item → Fabric data agent**, name `da_contoso_sql`, add `wh_contoso_cycles`, tick all six tables.
2. Switch the ribbon to **Build agent with AI** (preview) and ask:

```
Explore the schema. This is a bike distributor's sales and receivables data. Propose agent instructions, data source instructions and example queries so that "net sales" uses SalesOrderLine.Amount (excluding VAT), "overdue" means RemainingAmount > 0 and DueDate more than 5 days before 2026-11-20, and "on hold" refers to Customer.Status.
```

3. Review each suggestion and **Accept** the ones you agree with. Switch to **Test data agent**.

Notice what's different: on SQL sources the agent has **data source instructions** and **example queries**. On a semantic model it doesn't: that job belongs to Prep for AI.

## ✅ Checkpoint 3

Both agents answer *How many customers are there?* with **400**.
