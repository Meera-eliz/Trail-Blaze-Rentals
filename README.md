# 🚗 Trail Blaze Rentals

**Trail Blaze Rentals** is a full-featured luxury car rental website where users can explore a premium fleet, view pricing, create accounts, and manage payments. Built with a modern UI and integrated with a Python Flask backend for transaction processing.

---

## 📂 Project Structure

- `Home.html` – Landing page showcasing services and fleet highlights  
- `fleetpage.html` – Detailed vehicle listings with filter options  
- `aboutus.html` – Company mission, stats, awards, and testimonials  
- `createanaccount.html` – User registration form with validation  
- `index.html` – Admin payment dashboard  
- `home.css` – Styling for all frontend pages  
- `app.py` – Flask backend handling transactions with MySQL  

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS (custom + Bootstrap)
- **Backend:** Python Flask
- **Database:** MySQL (via PyMySQL)
- **Styling Tools:** Google Fonts, Font Awesome, Tailwind CSS (for dashboard)

---

## 🚀 Running the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/trail-blaze-rentals.git
   cd trail-blaze-rentals
2. **Install Python dependencies**
   ```bash
   pip install flask pymysql
   
3. **Set up MySQL database**
   - Create a MySQL database and configure it with your `app.py` for transactions.
   - Ensure that your database includes tables for users, vehicles, and transactions.

4. **Run the Flask server**
   ```bash
   python app.py

