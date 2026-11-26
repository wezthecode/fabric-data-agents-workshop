# 4. Test and tune: the wrong place to fix it

[Workshop home](../README.md) · Back: [3. Build two ways](03-build-two-ways.md) · Next: [5. Copilot Studio](05-copilot-studio.md)

## Before

In `da_contoso_semantic`, ask each question in a **new chat**, and expand the steps under each answer to see the DAX:

```
1. What were total net sales in 2025?
2. Which product category sold the most in 2026 so far?
3. How much is overdue right now?
4. What is 2026 bike revenue by customer segment?
5. How many customers are on hold?
6. How many open sales orders are there?
```

Compare with [expected-answers.md](../dataset/expected-answers.md). Questions 1 and 3 are the usual casualties: gross instead of net, and "past due" instead of "more than 5 days past due".

## The wrong place

Put the rule in the data agent's **Agent instructions**:

```
Overdue means an open invoice balance (Invoice[RemainingAmount] > 0) more than 5 days past Invoice[DueDate], as of 2026-11-20.
```

Ask question 3 again in a new chat. **The DAX doesn't change.** For semantic models, the DAX tool reads the model's metadata and Prep for AI, not the agent's instructions.

## The right place

1. `sm_contoso_cycles` → **Prep data for AI → Add AI instructions**, paste, **Apply**:

```
- "Sales", "revenue" or "net sales" means the Net Sales measure (SalesOrderLine[Amount], excluding VAT), by order date.
- Invoice[Amount] is gross including 23% VAT. Only use it when the user asks about invoiced or gross amounts.
- "Overdue" means the Overdue Balance measure: open invoice balance more than 5 days past the due date, as of 2026-11-20.
- "Customer status" or "on hold" refers to Customer[Status]. "Open orders" refers to SalesOrderHeader[Status] = "Open". Invoice[Status] is payment status only.
- "Segment" is Customer[Segment]. "Category" is Item[Category].
```

2. Add the measure and column **descriptions** from [module 1](01-semantic-model.md) too.
3. New chat, ask all six again.

## ✅ Checkpoint 4

All six answers match [expected-answers.md](../dataset/expected-answers.md). Then **Publish** the agent with a description, for example:

```
Answers questions about Contoso Cycle Supply's sales orders, customers, products and invoices (synthetic workshop data, Jan 2024 to Nov 2026): net sales, category and segment revenue, customer status, open orders and overdue balances.
```
