def calculate_gst(taxable_value, gst_rate, intra_state=True):
    """Educational GST calculator.
    gst_rate should be supplied as a decimal, e.g. 0.18 for 18%.
    """
    gst = taxable_value * gst_rate
    if intra_state:
        return {"taxable_value": taxable_value, "cgst": gst/2, "sgst": gst/2,
                "igst": 0, "invoice_total": taxable_value + gst}
    return {"taxable_value": taxable_value, "cgst": 0, "sgst": 0,
            "igst": gst, "invoice_total": taxable_value + gst}

if __name__ == "__main__":
    result = calculate_gst(10000, 0.18, intra_state=True)
    for key, value in result.items():
        print(f"{key}: ₹{value:,.2f}")
