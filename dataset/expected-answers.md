# Expected answers (generated, do not edit by hand)

Dataset: Contoso Cycle Supply, seed 2027, as-of date **2026-11-20**. Regenerate with `python3 generate.py`.

Rows: 400 customers, 198 items, 20,183 sales orders, 70,651 order lines, 19,898 invoices, 1,096 dates.

| # | Question | Correct answer | The trap |
|---|---|---|---|
| 1 | What were total net sales in 2025? | **83,987,558.66** (sum of SalesOrderLine[Amount] for 2025 orders) | Using Invoice[Amount] gives 103,116,337.98 for 2025 invoices: that's **gross incl. VAT**, by invoice date |
| 2 | Which product category sold the most in 2026 so far? | **Bikes** (47,941,774.56) | None: a warm-up both agents should get right |
| 3 | How much is overdue right now? | **20,084,575.48** across 360 customers (open balance more than 5 days past due) | Simply past due gives 20,475,382.79. The business definition has to come from Prep for AI |
| 4 | 2026 bike revenue by customer segment? | **Wholesale** 31,544,196.35, **Retail** 13,090,010.60, **Online** 3,307,567.61 | Needs Customer -> Order -> Line -> Item |
| 5 | How many customers are on hold? | **25** (Customer[Status] = On Hold) | 'Status' also exists on orders and invoices |
| 6 | How many open sales orders are there? | **60** (SalesOrderHeader[Status] = Open) | An 'open' invoice is a different thing |
