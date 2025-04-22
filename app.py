from flask import Flask, render_template, request, jsonify
import logging  # Change this import to use Python's built-in logging
import pymysql
from datetime import datetime

app = Flask(__name__)

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root1234",
    "database": "finalpayment"
}

# Configure logging properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
                transactions = cursor.fetchall()
                # Convert Decimal objects to float for JSON serialization
                for transaction in transactions:
                    transaction['amount'] = float(transaction['amount'])
                    transaction['created_at'] = transaction['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                return jsonify(transactions), 200
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        return jsonify({"error": "Failed to fetch transactions"}), 500

@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        logger.info(f"Received transaction data: {data}")
        
        # Validate required fields
        required_fields = ['customer', 'amount', 'payment_method']
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Validate payment method
        if data['payment_method'] not in ['Cash', 'Card', 'Online']:
            return jsonify({"error": "Invalid payment method. Must be Cash, Card, or Online"}), 400

        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({"error": "Amount must be greater than 0"}), 400
        except ValueError:
            return jsonify({"error": "Invalid amount format"}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO transactions (customer, amount, payment_method, status)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data['customer'],
                    amount,
                    data['payment_method'],
                    data.get('status', 'pending')
                ))
                conn.commit()
                
                # Get the ID of the inserted transaction
                transaction_id = cursor.lastrowid
                
                logger.info(f"Transaction added successfully. ID: {transaction_id}")
                return jsonify({
                    "message": "Transaction added successfully",
                    "transaction_id": transaction_id
                }), 201
    except Exception as e:
        logger.error(f"Error adding transaction: {str(e)}")
        return jsonify({"error": "Failed to add transaction"}), 500

@app.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
                transaction = cursor.fetchone()
                if transaction:
                    transaction['amount'] = float(transaction['amount'])
                    transaction['created_at'] = transaction['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    return jsonify(transaction), 200
                return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching transaction {id}: {str(e)}")
        return jsonify({"error": f"Failed to fetch transaction {id}"}), 500

@app.route('/transactions/update/<int:id>', methods=['PUT'])
def update_transaction(id):
    try:
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({"error": "Status is required"}), 400
            
        if status not in ['pending', 'completed', 'failed']:
            return jsonify({"error": "Invalid status. Must be pending, completed, or failed"}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # First check if transaction exists
                cursor.execute("SELECT id FROM transactions WHERE id = %s", (id,))
                if not cursor.fetchone():
                    return jsonify({"error": "Transaction not found"}), 404
                    
                sql = "UPDATE transactions SET status = %s WHERE id = %s"
                cursor.execute(sql, (status, id))
                conn.commit()
                
                logger.info(f"Transaction {id} updated successfully")
                return jsonify({"message": f"Transaction {id} updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating transaction {id}: {str(e)}")
        return jsonify({"error": f"Failed to update transaction {id}"}), 500

if __name__ == '__main__':
    app.run(debug=True)