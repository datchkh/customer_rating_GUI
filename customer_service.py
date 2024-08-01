import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('new_customer_service.db')
c = conn.cursor()

# Create a table to store customer reviews
c.execute('''CREATE TABLE IF NOT EXISTS reviews (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name TEXT NOT NULL,
                 last_name TEXT NOT NULL,
                 purchased_item TEXT NOT NULL,
                 rating INTEGER NOT NULL,
                 reason TEXT NOT NULL
             )''')

# Function to add a new review
def add_review(first_name, last_name, purchased_item, rating, reason):
    with conn:
        c.execute("INSERT INTO reviews (first_name, last_name, purchased_item, rating, reason) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, purchased_item, rating, reason))

# Function to display all reviews
def display_reviews():
    c.execute("SELECT * FROM reviews")
    reviews = c.fetchall()
    return reviews

# Function to delete a review by ID
def delete_review(review_id):
    with conn:
        c.execute("DELETE FROM reviews WHERE id = ?", (review_id,))

# Function to export reviews to a CSV file
def export_reviews_to_csv(filename):
    c.execute("SELECT * FROM reviews")
    reviews = c.fetchall()
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'First Name', 'Last Name', 'Purchased item', 'Rating', 'Reason'])  # Write headers
        csvwriter.writerows(reviews)  # Write data

# GUI application
class ReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Review Management")

        # Labels and entries for adding reviews
        self.first_name_label = tk.Label(root, text="First Name:")
        self.first_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.first_name_entry = tk.Entry(root)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.last_name_label = tk.Label(root, text="Last Name:")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.last_name_entry = tk.Entry(root)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.purchased_item_entry = tk.Label(root, text="Purchased item:")
        self.purchased_item_entry.grid(row=2, column=0, padx=5, pady=5)
        self.purchased_item_entry = tk.Entry(root)
        self.purchased_item_entry.grid(row=2, column=1, padx=5, pady=5)

        self.rating_label = tk.Label(root, text="Rating (1-5):")
        self.rating_label.grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        self.reason_label = tk.Label(root, text="Reason:")
        self.reason_label.grid(row=4, column=0, padx=5, pady=5)
        self.reason_entry = tk.Entry(root)
        self.reason_entry.grid(row=4, column=1, padx=5, pady=5)

        # Button for submitting review
        self.submit_button = tk.Button(root, text="Submit Review", command=self.submit_review)
        self.submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Button for exporting reviews to CSV
        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Button for displaying all reviews
        self.display_button = tk.Button(root, text="Display Reviews", command=self.display_reviews)
        self.display_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Text area to display reviews (wider)
        self.reviews_text = tk.Text(root, width=100, height=10)
        self.reviews_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Label and entry for deleting review by ID
        self.delete_id_label = tk.Label(root, text="Review ID to delete:")
        self.delete_id_label.grid(row=9, column=0, padx=5, pady=5)
        self.delete_id_entry = tk.Entry(root)
        self.delete_id_entry.grid(row=9, column=1, padx=5, pady=5)

        # Button for deleting review
        self.delete_button = tk.Button(root, text="Delete Review", command=self.delete_review)
        self.delete_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

    def submit_review(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        purchased_item = self.purchased_item_entry.get()
        rating = self.rating_entry.get()
        reason = self.reason_entry.get()

        if not first_name or not last_name or not rating.isdigit() or not reason:
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        add_review(first_name, last_name, purchased_item, int(rating), reason)
        messagebox.showinfo("Success", "Review submitted successfully!")

        # Clear entries
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.purchased_item_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)

    def export_to_csv(self):
        export_reviews_to_csv('new_customer_reviews.csv')
        messagebox.showinfo("Success", "Reviews exported to new_customer_reviews.csv")

    def display_reviews(self):
        reviews = display_reviews()
        self.reviews_text.delete(1.0, tk.END)
        for review in reviews:
            self.reviews_text.insert(tk.END, f"ID: {review[0]}, First Name: {review[1]}, Last Name: {review[2]}, Purchased item, {review[3]} Rating: {review[4]}, Reason: {review[5]}\n -------------------------------------------\n")

    def delete_review(self):
        review_id = self.delete_id_entry.get()
        if not review_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid ID.")
            return

        delete_review(int(review_id))
        messagebox.showinfo("Success", "Review deleted successfully!")
        self.delete_id_entry.delete(0, tk.END)
        self.display_reviews()

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = ReviewApp(root)
    root.mainloop()

    # Close the database connection when the app is closed
    conn.close()
