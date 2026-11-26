# 1. Build the semantic model

[Workshop home](../README.md) · Back: [0. Setup](00-setup.md) · Next: [2. Prep for AI](02-prep-for-ai.md)

1. Open `lh_contoso_cycles` → **New semantic model**. Name it `sm_contoso_cycles`, tick all six tables, **Confirm** (Direct Lake).
2. **Open data model** and switch to **Editing** (top right).
3. **Rename the tables** to `Customer`, `Item`, `SalesOrderHeader`, `SalesOrderLine`, `Invoice`, `Date`. The questions and instructions use these names.
4. **Relationships:** drag from the many side to the one side. Many to one, single direction, **Assume referential integrity**:

```
SalesOrderHeader[CustomerID]   ->  Customer[CustomerID]
SalesOrderLine[SalesOrderID]   ->  SalesOrderHeader[SalesOrderID]
SalesOrderLine[ItemID]         ->  Item[ItemID]
Invoice[CustomerID]            ->  Customer[CustomerID]
SalesOrderHeader[OrderDate]    ->  Date[Date]
```

   Don't relate Invoice to SalesOrderHeader: it gives Invoice two paths to Customer.
5. **Measures** (New measure): `Net Sales` on SalesOrderLine, the other two on Invoice:

```dax
Net Sales = SUM ( SalesOrderLine[Amount] )

Invoiced Gross = SUM ( Invoice[Amount] )

Overdue Balance =
CALCULATE (
    SUM ( Invoice[RemainingAmount] ),
    Invoice[RemainingAmount] > 0,
    Invoice[DueDate] < DATE ( 2026, 11, 20 ) - 5
)
```

6. **Descriptions** (Properties pane → Description). Add the **table** descriptions now. Keep the measure and column ones for module 4, so the "before" run shows the traps:

```
TABLES
Customer          One row per customer: name, country, segment, credit limit, payment terms and account status.
Item              One row per product: name, category, subcategory, list price and unit cost.
SalesOrderHeader  One row per sales order: customer, order date and order status. Use for order counts and order dates.
SalesOrderLine    One row per order line: item, quantity, price, discount and net line amount. The source for net sales.
Invoice           One row per invoice: invoice, due and paid dates, gross amount including VAT, remaining balance and payment status.
Date              Calendar table, 2024 to 2026. Filters sales by order date.

MEASURES
Net Sales         Net sales excluding VAT, from order lines, by order date. Use for "sales", "revenue" or "net sales".
Invoiced Gross    Total invoiced amount including 23% VAT, by invoice. Use only when asked for invoiced or gross amounts.
Overdue Balance   Open invoice balance more than 5 days past the due date, as of 2026-11-20. Use for "overdue".

COLUMNS
Customer[Status]             Customer account status: Active or On Hold. Use for "customers on hold".
Customer[Segment]            Customer segment: Retail, Wholesale or Online.
Item[Category]               Product category: Bikes, Components, Apparel or Accessories.
SalesOrderHeader[Status]     Order status: Open, Released, Shipped or Invoiced. Use for "open orders".
SalesOrderHeader[NetAmount]  Order total excluding VAT. Use the Net Sales measure for sales totals.
SalesOrderLine[Amount]       Net line amount after discount, excluding VAT.
Invoice[Amount]              Gross invoice amount including 23% VAT. Not net sales.
Invoice[RemainingAmount]     Amount still unpaid on the invoice. 0 means fully paid.
Invoice[DueDate]             Date payment is due. Overdue means more than 5 days past this date.
Invoice[Status]              Payment status: Paid, Open or Partially Paid. Not the order status.
```

## ✅ Checkpoint 1

In **DAX query view**, run:

```dax
EVALUATE
ROW (
    "Net sales 2025", CALCULATE ( [Net Sales], 'Date'[Year] = 2025 ),
    "Overdue", [Overdue Balance],
    "On hold", CALCULATE ( COUNTROWS ( Customer ), Customer[Status] = "On Hold" )
)
```

Expect **83,987,558.66 · 20,084,575.48 · 25**.
