# 0. Set up and load the data

[Workshop home](../README.md) · Next: [1. Semantic model](01-semantic-model.md)

1. **Workspace:** in Fabric, **Workspaces → + New workspace**. Under **Advanced → License mode**, pick your paid **Fabric capacity**.
2. **Get the data:** download [`dataset/contoso-cycle-supply-csv.zip`](../dataset/contoso-cycle-supply-csv.zip) and unzip it.
3. **Lakehouse:** **+ New item → Lakehouse**, name it `lh_contoso_cycles`, leave **Lakehouse schemas** off.
4. In the Explorer, **… next to Files → Upload → Upload files**, select all six CSVs.
5. On the lakehouse ribbon, **Open notebook → New notebook** (it opens attached to the lakehouse). Paste this cell and **Run all**:

```python
from pyspark.sql import functions as F

tables = {
    "Customer": ("customer", []),
    "Item": ("item", []),
    "SalesOrderHeader": ("sales_order_header", ["OrderDate"]),
    "SalesOrderLine": ("sales_order_line", []),
    "Invoice": ("invoice", ["InvoiceDate", "DueDate", "PaidDate"]),
    "Date": ("calendar_date", ["Date"]),
}

for csv_name, (table, date_cols) in tables.items():
    df = (spark.read.option("header", True).option("inferSchema", True)
          .csv(f"Files/{csv_name}.csv"))
    for c in date_cols:
        df = df.withColumn(c, F.to_date(F.col(c).cast("string")))
    (df.write.mode("overwrite").option("overwriteSchema", "true")
       .format("delta").saveAsTable(table))
    print(table, df.count())
```

   The **Load to Tables** button would also work, but it can't set column types, and the overdue measure needs real dates.
6. **Stop session** on the notebook toolbar when it's done.

## Warehouse copy (for module 3)

**Build agent with AI** only works on SQL sources, so make a warehouse copy:

1. **+ New item → Warehouse**, name it `wh_contoso_cycles`.
2. In its Explorer, **+ Warehouses** and add the `lh_contoso_cycles` SQL analytics endpoint.
3. **New SQL query**, paste and run:

```sql
CREATE TABLE dbo.Customer         AS SELECT * FROM lh_contoso_cycles.dbo.customer;
CREATE TABLE dbo.Item             AS SELECT * FROM lh_contoso_cycles.dbo.item;
CREATE TABLE dbo.SalesOrderHeader AS SELECT * FROM lh_contoso_cycles.dbo.sales_order_header;
CREATE TABLE dbo.SalesOrderLine   AS SELECT * FROM lh_contoso_cycles.dbo.sales_order_line;
CREATE TABLE dbo.Invoice          AS SELECT * FROM lh_contoso_cycles.dbo.invoice;
CREATE TABLE dbo.[Date]           AS SELECT * FROM lh_contoso_cycles.dbo.calendar_date;
```

## ✅ Checkpoint 0

```sql
SELECT 'Customer' AS t, COUNT(*) AS n FROM dbo.Customer
UNION ALL SELECT 'Item', COUNT(*) FROM dbo.Item
UNION ALL SELECT 'SalesOrderHeader', COUNT(*) FROM dbo.SalesOrderHeader
UNION ALL SELECT 'SalesOrderLine', COUNT(*) FROM dbo.SalesOrderLine
UNION ALL SELECT 'Invoice', COUNT(*) FROM dbo.Invoice
UNION ALL SELECT 'Date', COUNT(*) FROM dbo.[Date];
```

Expect 400 · 198 · 20,183 · 70,651 · 19,898 · 1,096. If the lakehouse tables don't show up in SQL yet, open its SQL analytics endpoint and select **Refresh**.
