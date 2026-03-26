from data import SALES_DATA

def get_sales_by_month(month: str) -> dict:
    """Returns total revenue and units sold for a given month."""
    month = month.capitalize()
    results = [row for row in SALES_DATA if row["month"] == month]
    if not results:
        return {"error": f"No data found for month: {month}"}
    total_revenue = sum(r["revenue"] for r in results)
    total_units = sum(r["units"] for r in results)
    return {
        "month": month,
        "total_revenue": total_revenue,
        "total_units": total_units,
        "breakdown": results
    }

def get_top_product(month: str = None) -> dict:
    """Returns the best-selling product by revenue. Optionally filtered by month."""
    data = SALES_DATA
    if month:
        month = month.capitalize()
        data = [r for r in data if r["month"] == month]
    if not data:
        return {"error": "No data found"}
    
    product_totals = {}
    for row in data:
        p = row["product"]
        product_totals[p] = product_totals.get(p, 0) + row["revenue"]

    top = max(product_totals, key=product_totals.get)
    return {
        "top_product": top,
        "revenue": product_totals[top],
        "filter": month if month else "all time"
    }

def compare_months(month_a: str, month_b: str) -> dict:
    """Compare total revenue between two months."""
    month_a = month_a.capitalize()
    month_b = month_b.capitalize()

    rev_a = sum(r["revenue"] for r in SALES_DATA if r["month"] == month_a)
    rev_b = sum(r["revenue"] for r in SALES_DATA if r["month"] == month_b)

    if rev_a == 0 and rev_b == 0:
        return {"error": "No data for either month"}

    difference = rev_a - rev_b
    pct_change = round((difference / rev_b * 100), 1) if rev_b else 0

    return {
        "month_a": month_a,
        "revenue_a": rev_a,
        "month_b": month_b,
        "revenue_b": rev_b,
        "difference": difference,
        "percent_change": pct_change
    }

def get_total_revenue() -> dict:
    """Returns total revenue across all months and products."""
    total = sum(r["revenue"] for r in SALES_DATA)
    total_units = sum(r["units"] for r in SALES_DATA)
    return {
        "total revenue": total,
        "total_units": total_units,
        "months_covered": list(dict.fromkeys(r["month"] for r in SALES_DATA))
    }