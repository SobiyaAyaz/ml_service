UPI_KEYWORDS = [
    "phonepe", "paytm", "bhim", "gpay", "google pay",
    "sbi", "hdfc", "icici", "upi", "payment", "qr",
    "razorpay", "mobikwik", "freecharge", "airtel money"
]

def is_upi_fraud_domain(url_or_text: str) -> dict:
    """
    Checks if a URL or VirusTotal result contains UPI/Indian payment keywords.
    Returns a dict with flag and matched keywords.
    """
    text = url_or_text.lower()
    matched = [kw for kw in UPI_KEYWORDS if kw in text]
    return {
        "is_upi_fraud": len(matched) > 0,
        "matched_keywords": matched,
        "message": (
            f"Warning: This may be a UPI fraud attempt. Keywords found: {', '.join(matched)}"
            if matched else "No UPI fraud indicators found."
        )
    }