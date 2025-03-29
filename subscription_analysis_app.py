import pandas as pd
import pdfplumber
import re
import streamlit as st

# Function to extract transactions from PDF
def extract_transactions_from_pdf(pdf_file):
    transactions = []
    date_pattern = r"(\d{1,2} \w{3}, \d{4})"
    amount_pattern = r"([-+]?\d{1,3}(?:,\d{3})*\.\d{2})"

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    date_match = re.search(date_pattern, line)
                    amount_match = re.findall(amount_pattern, line)

                    if date_match and amount_match:
                        date = date_match.group(1)
                        amount = amount_match[-1].replace(",", "")
                        description = line.replace(date, "").strip()
                        description = re.sub(amount_pattern, "", description).strip()

                        transactions.append([date, description, float(amount)])

    df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(inplace=True)

    return df

# Function to categorize transactions
def categorize_transactions(df):
    categories = {
        "Entertainment": ["netflix", "spotify", "youtube", "disney+"],
        "Shopping": ["amazon", "ebay"],
        "Utilities": ["electric", "water", "internet"],
    }
    df["Category"] = "Other"
    for category, keywords in categories.items():
        mask = df["Description"].str.lower().str.contains("|".join(keywords), case=False, na=False)
        df.loc[mask, "Category"] = category
    return df

# Function to detect subscriptions
def detect_subscriptions(df):
    subscription_keywords = ["netflix", "spotify", "amazon prime", "youtube premium", "apple music", "hulu", "disney+", "patreon"]
    df["is_subscription"] = df["Description"].str.contains('|'.join(subscription_keywords), case=False, na=False)
    return df[df["is_subscription"]]

# Streamlit UI
st.title("📊 Subscription Spending Tracker")

# 💰 Budget Section
budget = st.number_input("💰 Set Monthly Budget (PKR)", min_value=0, value=5000)

# User Input Option
option = st.radio("📥 Select input method:", ("Upload PDF", "Upload CSV", "Enter Manually"))

df = None  # Placeholder for DataFrame

if option == "Upload PDF":
    pdf_file = st.file_uploader("📂 Upload your bank statement (PDF)", type=["pdf"])
    if pdf_file:
        df = extract_transactions_from_pdf(pdf_file)

elif option == "Upload CSV":
    csv_file = st.file_uploader("📂 Upload your transactions (CSV)", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

elif option == "Enter Manually":
    st.write("📝 Enter your transactions below:")
    manual_data = st.text_area("Enter transactions in the format: Date, Description, Amount (one per line)")

    if manual_data:
        data = [line.strip().split(",") for line in manual_data.split("\n") if line]
        df = pd.DataFrame(data, columns=["Date", "Description", "Amount"])
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df.dropna(inplace=True)

# Ensure df is available before processing
if df is not None and not df.empty:
    # Categorize transactions before processing
    df = categorize_transactions(df)
    
    # Detect subscriptions
    sub_df = detect_subscriptions(df)
    total_spent = sub_df["Amount"].sum() if not sub_df.empty else 0

    # 📅 Monthly Spending Summary
    df["Month"] = df["Date"].dt.to_period("M")
    monthly_spending = df.groupby("Month")["Amount"].sum()

    # Show warning if over budget
    for month, amount in monthly_spending.items():
        if amount > budget:
            st.warning(f"⚠️ You exceeded your budget of PKR {budget} in {month} with PKR {amount} spent!")
        else:
            st.success(f"✅ You stayed within your budget of PKR {budget} in {month}, spending PKR {amount}.")

    st.write("### 📅 Monthly Spending Summary")
    st.bar_chart(monthly_spending)

    # 📊 Show Subscription Spending Data
    st.write(f"### 💰 Total Subscription Spending: PKR {total_spent:.2f}")
    st.dataframe(sub_df)

    # 📊 Category-wise Spending
    if "Category" in df.columns:
        category_spending = df.groupby("Category")["Amount"].sum()
        if not category_spending.empty:
            st.write("### 📊 Spending by Category")
            st.bar_chart(category_spending)
        else:
            st.write("No categorized transactions available.")
    else:
        st.write("⚠️ Error: 'Category' column is missing.")
