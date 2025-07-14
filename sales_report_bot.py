import pandas as pd
from fpdf import FPDF

# ========== 1. LOAD DATA ==========
df = pd.read_csv("sales_data.csv")

# ========== 2. CHATBOT ==========
print("🤖 Hello! I can generate a sales report for you.")
user_input = input("What would you like to include? (total sales, top product, daily breakdown): ").lower()

# ========== 3. ANALYSIS ==========
report_lines = []

if "total sales" in user_input:
    total_revenue = df["Revenue"].sum()
    report_lines.append(f"📊 Total Revenue: ${total_revenue:.2f}")

if "top product" in user_input:
    top_product = df.groupby("Product")["Revenue"].sum().idxmax()
    top_revenue = df.groupby("Product")["Revenue"].sum().max()
    report_lines.append(f"🏆 Top Product: {top_product} (${top_revenue:.2f})")

if "daily" in user_input:
    daily_summary = df.groupby("Date")["Revenue"].sum().reset_index()
    report_lines.append("📅 Daily Breakdown:")
    for _, row in daily_summary.iterrows():
        report_lines.append(f"  {row['Date']}: ${row['Revenue']:.2f}")

# ========== 4. GENERATE PDF ==========
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "📄 Sales Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in report_lines:
    pdf.multi_cell(0, 10, line)

output_file = "sales_report.pdf"
pdf.output(output_file)
print(f"✅ Report generated: {output_file}")
