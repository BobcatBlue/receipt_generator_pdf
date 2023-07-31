import pandas as pd
from fpdf import FPDF


class Purchase:
    def __init__(self, item_no, df):
        self.item_no = item_no
        self.article_name = df.loc[df["id"] == self.item_no, "name"].squeeze().title()
        self.price = df.loc[df["id"] == self.item_no, "price"].squeeze()
        self.quantity = int(df.loc[df["id"] == self.item_no, "in stock"].squeeze())
        self.inventory = df

    def available(self):
        return self.quantity

    def update_inventory(self):
        self.inventory.loc[inventory["id"] == self.item_no, "in stock"] = self.quantity - 1
        self.inventory.to_csv("articles.csv", index=False)


class Receipt:
    def __init__(self, purchase_object):
        self.purchase_info = purchase_object

    def generate_receipt(self):
        receipt_line = f"Receipt No. {self.purchase_info.item_no}"
        article_line = f"Article:  {self.purchase_info.article_name}"
        price_line = f"Price:  ${self.purchase_info.price}"

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=9, txt=receipt_line, ln=1, align="L")
        pdf.cell(w=50, h=9, txt=article_line, ln=1, align="L")
        pdf.cell(w=50, h=9, txt=price_line, ln=1, align="L")

        pdf.output("Receipt.pdf")


inventory = pd.read_csv("articles.csv", dtype={"id": str, "price": str})

print(inventory)

while True:
    item_id = input("Enter the ID of the item you'd like to purchase: ")
    purchase = Purchase(item_no=item_id, df=inventory)

    if purchase.available():
        purchase.update_inventory()
        Receipt(purchase).generate_receipt()
        break
    else:
        print("This item is out of stock :(")
