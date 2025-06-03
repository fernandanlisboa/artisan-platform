# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 
import os 
from sqlalchemy.exc import OperationalError, InterfaceError, ArgumentError # SQLAlchemy exceptions
from sqlalchemy import text
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Flask configurations
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        if os.getenv('CHECK_DB_CONNECTION_ON_STARTUP', 'False') == 'True': # Controlled by environment variable
            try:
                # Try a lightweight operation to check connectivity
                with db.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                print("INFO: Database connection successfully verified!")
            except ArgumentError as ae: # Errors in DATABASE_URL formatting
                print(f"CONFIGURATION ERROR: Invalid DATABASE_URL format: {ae}")
                print("ACTION: Check the syntax of DATABASE_URL in your .env (e.g., mysql+pymysql://user:pass@host/db).")
            except OperationalError as oe: # Operational errors: connection refused, access denied, unknown DB
                # oe.orig often contains the original driver exception (e.g., pymysql.err.OperationalError)
                original_exception_msg = str(oe.orig) if oe.orig else str(oe)
                print(f"OPERATIONAL ERROR: Failed to connect to the database: {original_exception_msg}")
                
                if "1045" in original_exception_msg: # MySQL error code for Access Denied
                    print("LIKELY CAUSE: Access denied. Check user, password, source host, and database permissions.")
                elif "1049" in original_exception_msg: # MySQL error code for Unknown database
                    print("LIKELY CAUSE: Database not found. Check the database name in DATABASE_URL.")
                elif "2003" in original_exception_msg or "2005" in original_exception_msg: # Codes for "Can't connect to MySQL server"
                    print("LIKELY CAUSE: Could not connect to MySQL server. Check host, port, if the server is running, and if applicable, if the Cloud SQL Auth Proxy is active and properly configured.")
                else:
                    print("ACTION: Check DATABASE_URL, database server status, network settings (e.g., Cloud SQL 'Authorized Networks', Proxy status), and application logs for more details.")
            except InterfaceError as ie: # Problems with the DBAPI interface (e.g., driver not found)
                print(f"DB INTERFACE ERROR: Problem with the database driver (e.g., pymysql): {ie}")
                print("ACTION: Check if the database driver (such as pymysql) is correctly installed in the application environment.")
            except Exception as e: # Other unexpected errors
                print(f"UNEXPECTED ERROR while trying to connect to the database: {e}")
                print("ACTION: Check general settings and application logs.")
        
    return app