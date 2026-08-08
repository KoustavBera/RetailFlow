-- Schema definition for RetailFlow data warehouse

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_products (
    stock_code VARCHAR(50) PRIMARY KEY,
    description TEXT,
    unit_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
    transaction_id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50) NOT NULL,
    stock_code VARCHAR(50) REFERENCES dim_products(stock_code),
    customer_id INT REFERENCES dim_customers(customer_id),
    quantity INT NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
