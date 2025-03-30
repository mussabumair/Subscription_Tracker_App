# Subscription Spending Tracker

## 📌 Overview

The **Subscription Spending Tracker** is a financial web application built using **Streamlit** that helps users monitor their recurring expenses. The app allows users to upload bank statements, automatically detect subscription-based transactions, and visualize spending trends over time.

## 🚀 Features

- **Upload Transactions**: Supports both **PDF** and **CSV** file formats.
- **Manual Entry**: Allows users to input transactions manually.
- **Automatic Subscription Detection**: Identifies subscriptions like Netflix, Spotify, Amazon Prime, etc.
- **Monthly Budgeting**: Compares spending against a set budget and alerts if exceeded.
- **Spending Visualization**: Interactive bar charts for **monthly spending** and **category-wise analysis**.
- **Custom Background Support**: Enhances the UI with a personalized background image.

## 📂 Installation & Setup

To run this project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/subscription-tracker.git
   cd subscription-tracker
   ```

2. **Create a virtual environment (Optional but recommended):**

   ```bash
   python -m venv env
   source env/bin/activate  # On macOS/Linux
   env\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

## 📜 Usage

1. Set your **monthly budget**.
2. Choose how to input transactions (**Upload PDF/CSV** or **Enter manually**).
3. View your **monthly spending summary**.
4. Get alerts if you **exceed your budget**.
5. Visualize **subscription spending trends**.
6. Analyze **category-wise spending**.

## 📌 Dependencies

- Python 3.x
- Streamlit
- Pandas
- pdfplumber
- re (Regular Expressions)
- base64 (For image encoding)

## 🎨 Adding a Custom Background Image

To set a background image, replace the `BACKGROUND.jpg` file in the project directory and update the filename in:

```python
add_local_background("BACKGROUND.jpg")
```

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

For any queries or feedback, feel free to reach out on **LinkedIn** or open an issue in the repository.

---

**Happy Budgeting! 💰📊**

