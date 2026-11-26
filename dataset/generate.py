"""Generate the clean-room 'Contoso Cycle Supply' dataset for the Fabric data agents workshop.

Standard library only. Deterministic (fixed seed), so every run gives the same data and the
same expected answers. Writes CSVs to ./output and the golden answers to ./expected-answers.md.

    python3 generate.py

Deliberate traps for module 4:
  1. Ambiguous names: 'Status' exists on Customer, SalesOrderHeader and Invoice, and
     'Amount' is NET on SalesOrderLine but GROSS (incl. VAT) on Invoice.
  2. A business definition: 'overdue' means an open balance more than 5 days past the due date,
     not simply past the due date.
  3. A relationship hop: revenue by customer segment for one item category needs
     Customer -> SalesOrderHeader -> SalesOrderLine -> Item.
"""

import csv
import datetime as dt
import os
import random

SEED = 2027
AS_OF = dt.date(2026, 11, 20)
START = dt.date(2024, 1, 1)
VAT = 0.23
OVERDUE_GRACE_DAYS = 5

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

rng = random.Random(SEED)

COUNTRIES = [("PT", "Portugal", 0.30), ("ES", "Spain", 0.22), ("FR", "France", 0.15),
             ("DE", "Germany", 0.13), ("NL", "Netherlands", 0.10), ("GB", "United Kingdom", 0.10)]
SEGMENTS = [("Retail", 0.5), ("Wholesale", 0.3), ("Online", 0.2)]
TERMS = [14, 30, 45, 60]
CATEGORIES = {
    "Bikes": (["Road", "Gravel", "City", "Mountain", "Electric", "Kids"], (450, 3200)),
    "Components": (["Chain", "Cassette", "Brake Set", "Wheelset", "Crankset", "Derailleur", "Saddle"], (25, 650)),
    "Apparel": (["Jersey", "Bib Shorts", "Rain Jacket", "Gloves", "Socks"], (12, 180)),
    "Accessories": (["Helmet", "Light Set", "Lock", "Pump", "Bottle Cage", "Bag"], (8, 220)),
}
SYL = ["ra", "lo", "ve", "ta", "mi", "no", "sa", "ber", "cor", "lin", "do", "ma", "zen", "qui", "por", "vel"]
SUFFIX = ["Cycles", "Bike Co", "Velo", "Sports", "Outdoor", "Ride Shop", "Trading", "Bikes"]


def pick_weighted(options):
    r = rng.random()
    acc = 0.0
    for opt in options:
        acc += opt[-1]
        if r <= acc:
            return opt
    return options[-1]


def name():
    return (rng.choice(SYL) + rng.choice(SYL) + rng.choice(SYL)).capitalize() + " " + rng.choice(SUFFIX)


def write(fname, header, rows):
    with open(os.path.join(OUT, fname), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    os.makedirs(OUT, exist_ok=True)

    # Customers
    customers = []
    for i in range(1, 401):
        code, country, _ = pick_weighted(COUNTRIES)
        segment = pick_weighted(SEGMENTS)[0]
        limit = {"Retail": 15000, "Wholesale": 60000, "Online": 8000}[segment] * rng.choice([0.5, 1, 1, 1.5, 2])
        status = "On Hold" if rng.random() < 0.06 else "Active"
        customers.append({
            "CustomerID": f"C{i:04d}", "CustomerName": name(), "CountryCode": code, "Country": country,
            "Segment": segment, "CreditLimit": round(limit, 2), "PaymentTermsDays": rng.choice(TERMS),
            "Status": status,
            "Weight": rng.paretovariate(1.6),  # a few big customers, many small ones
        })

    # Items
    items = []
    n = 1
    for cat, (models, (lo, hi)) in CATEGORIES.items():
        for model in models:
            for variant in range(rng.randint(5, 12)):
                price = round(rng.uniform(lo, hi), 2)
                items.append({
                    "ItemID": f"I{n:04d}", "ItemName": f"{model} {chr(65 + variant)}{rng.randint(10, 99)}",
                    "Category": cat, "SubCategory": model, "UnitPrice": price,
                    "UnitCost": round(price * rng.uniform(0.45, 0.75), 2),
                    "Weight": rng.paretovariate(1.8),
                })
                n += 1

    cust_w = [c["Weight"] for c in customers]
    item_w = [it["Weight"] for it in items]

    # Orders, lines and invoices
    headers, lines, invoices = [], [], []
    order_no = 1
    inv_no = 1
    day = START
    while day <= AS_OF:
        season = 1.0 + 0.45 * (day.month in (4, 5, 6, 7)) - 0.25 * (day.month in (12, 1))
        growth = 1.0 + 0.18 * ((day - START).days / 365.0)
        weekday = 0.35 if day.weekday() >= 5 else 1.0
        for _ in range(int(rng.gauss(17 * season * growth * weekday, 4)) if True else 0):
            c = rng.choices(customers, weights=cust_w)[0]
            oid = f"SO{order_no:06d}"
            order_no += 1
            age = (AS_OF - day).days
            if age > 21:
                status = "Invoiced"
            elif age > 7:
                status = rng.choice(["Shipped", "Invoiced", "Invoiced"])
            else:
                status = rng.choice(["Open", "Released", "Shipped"])
            net_total = 0.0
            for ln in range(1, rng.randint(1, 6) + 1):
                it = rng.choices(items, weights=item_w)[0]
                qty = rng.randint(1, 3) if it["Category"] == "Bikes" else rng.randint(1, 12)
                if c["Segment"] == "Wholesale":
                    qty *= rng.randint(2, 5)
                disc = rng.choice([0, 0, 0, 0.05, 0.1]) + (0.05 if c["Segment"] == "Wholesale" else 0)
                amount = round(qty * it["UnitPrice"] * (1 - disc), 2)
                net_total += amount
                lines.append([oid, ln, it["ItemID"], qty, it["UnitPrice"], round(disc, 2), amount])
            headers.append([oid, c["CustomerID"], day.isoformat(), status, round(net_total, 2)])

            if status == "Invoiced":
                inv_date = day + dt.timedelta(days=rng.randint(0, 6))
                if inv_date > AS_OF:
                    inv_date = AS_OF
                due = inv_date + dt.timedelta(days=c["PaymentTermsDays"])
                gross = round(net_total * (1 + VAT), 2)
                late_bias = 0.25 if c["Status"] == "On Hold" else 0.0
                r = rng.random()
                if r < 0.78 - late_bias:
                    paid = due + dt.timedelta(days=rng.randint(-10, 4))
                elif r < 0.93 - late_bias / 2:
                    paid = due + dt.timedelta(days=rng.randint(5, 75))
                else:
                    paid = None
                if paid is not None and paid > AS_OF:
                    paid = None
                if paid is None and rng.random() < 0.25:
                    remaining = round(gross * rng.choice([0.25, 0.5, 0.75]), 2)
                    inv_status = "Partially Paid"
                elif paid is None:
                    remaining = gross
                    inv_status = "Open"
                else:
                    remaining = 0.0
                    inv_status = "Paid"
                invoices.append([f"INV{inv_no:06d}", oid, c["CustomerID"], inv_date.isoformat(), due.isoformat(),
                                 paid.isoformat() if paid else "", gross, remaining, inv_status])
                inv_no += 1
        day += dt.timedelta(days=1)

    # Date table
    dates = []
    d = START
    while d <= dt.date(AS_OF.year, 12, 31):
        dates.append([d.isoformat(), d.year, (d.month - 1) // 3 + 1, d.month, d.strftime("%B"),
                      d.strftime("%Y-%m"), d.isocalendar()[1], d.strftime("%A")])
        d += dt.timedelta(days=1)

    write("Customer.csv", ["CustomerID", "CustomerName", "CountryCode", "Country", "Segment", "CreditLimit",
                           "PaymentTermsDays", "Status"],
          [[c[k] for k in ["CustomerID", "CustomerName", "CountryCode", "Country", "Segment", "CreditLimit",
                           "PaymentTermsDays", "Status"]] for c in customers])
    write("Item.csv", ["ItemID", "ItemName", "Category", "SubCategory", "UnitPrice", "UnitCost"],
          [[it[k] for k in ["ItemID", "ItemName", "Category", "SubCategory", "UnitPrice", "UnitCost"]] for it in items])
    write("SalesOrderHeader.csv", ["SalesOrderID", "CustomerID", "OrderDate", "Status", "NetAmount"], headers)
    write("SalesOrderLine.csv", ["SalesOrderID", "LineNo", "ItemID", "Quantity", "UnitPrice", "DiscountPct", "Amount"], lines)
    write("Invoice.csv", ["InvoiceID", "SalesOrderID", "CustomerID", "InvoiceDate", "DueDate", "PaidDate",
                          "Amount", "RemainingAmount", "Status"], invoices)
    write("Date.csv", ["Date", "Year", "Quarter", "MonthNo", "MonthName", "YearMonth", "ISOWeek", "DayName"], dates)

    # Golden answers
    cust = {c["CustomerID"]: c for c in customers}
    item = {it["ItemID"]: it for it in items}
    hdr = {h[0]: h for h in headers}

    def year_of(oid):
        return int(hdr[oid][2][:4])

    net_2025 = sum(l[6] for l in lines if year_of(l[0]) == 2025)
    cat_ytd = {}
    for l in lines:
        if year_of(l[0]) == 2026:
            cat = item[l[2]]["Category"]
            cat_ytd[cat] = cat_ytd.get(cat, 0) + l[6]
    top_cat = max(cat_ytd, key=cat_ytd.get)

    naive_overdue = sum(i[7] for i in invoices if i[7] > 0 and dt.date.fromisoformat(i[4]) < AS_OF)
    true_overdue = sum(i[7] for i in invoices if i[7] > 0 and
                       (AS_OF - dt.date.fromisoformat(i[4])).days > OVERDUE_GRACE_DAYS)
    overdue_customers = len({i[2] for i in invoices if i[7] > 0 and
                             (AS_OF - dt.date.fromisoformat(i[4])).days > OVERDUE_GRACE_DAYS})

    seg_bikes = {}
    for l in lines:
        if year_of(l[0]) == 2026 and item[l[2]]["Category"] == "Bikes":
            seg = cust[hdr[l[0]][1]]["Segment"]
            seg_bikes[seg] = seg_bikes.get(seg, 0) + l[6]

    net_inv_2025 = sum(i[6] for i in invoices if i[3][:4] == "2025")
    on_hold = sum(1 for c in customers if c["Status"] == "On Hold")
    open_orders = sum(1 for h in headers if h[3] == "Open")

    with open(os.path.join(HERE, "expected-answers.md"), "w", encoding="utf-8") as f:
        f.write("# Expected answers (generated, do not edit by hand)\n\n")
        f.write(f"Dataset: Contoso Cycle Supply, seed {SEED}, as-of date **{AS_OF.isoformat()}**. "
                "Regenerate with `python3 generate.py`.\n\n")
        f.write(f"Rows: {len(customers)} customers, {len(items)} items, {len(headers):,} sales orders, "
                f"{len(lines):,} order lines, {len(invoices):,} invoices, {len(dates):,} dates.\n\n")
        f.write("| # | Question | Correct answer | The trap |\n|---|---|---|---|\n")
        f.write(f"| 1 | What were total net sales in 2025? | **{net_2025:,.2f}** (sum of SalesOrderLine[Amount] for 2025 orders) | "
                f"Using Invoice[Amount] gives {net_inv_2025:,.2f} for 2025 invoices: that's **gross incl. VAT**, by invoice date |\n")
        f.write(f"| 2 | Which product category sold the most in 2026 so far? | **{top_cat}** ({cat_ytd[top_cat]:,.2f}) | "
                "None: a warm-up both agents should get right |\n")
        f.write(f"| 3 | How much is overdue right now? | **{true_overdue:,.2f}** across {overdue_customers} customers "
                f"(open balance more than {OVERDUE_GRACE_DAYS} days past due) | Simply past due gives {naive_overdue:,.2f}. "
                "The business definition has to come from Prep for AI |\n")
        f.write("| 4 | 2026 bike revenue by customer segment? | " +
                ", ".join(f"**{k}** {v:,.2f}" for k, v in sorted(seg_bikes.items(), key=lambda kv: -kv[1])) +
                " | Needs Customer -> Order -> Line -> Item |\n")
        f.write(f"| 5 | How many customers are on hold? | **{on_hold}** (Customer[Status] = On Hold) | "
                "'Status' also exists on orders and invoices |\n")
        f.write(f"| 6 | How many open sales orders are there? | **{open_orders}** (SalesOrderHeader[Status] = Open) | "
                "An 'open' invoice is a different thing |\n")


if __name__ == "__main__":
    main()
