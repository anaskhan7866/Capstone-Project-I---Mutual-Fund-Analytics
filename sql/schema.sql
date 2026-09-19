-- Dimension: Fund
CREATE TABLE dim_fund (
    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code VARCHAR(10) UNIQUE NOT NULL,
    scheme_name VARCHAR(255) NOT NULL,
    fund_house VARCHAR(100),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    risk_grade VARCHAR(20)
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Fact: NAV
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    date_id INTEGER,
    nav REAL NOT NULL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Fact: Transactions
CREATE TABLE fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    date_id INTEGER,
    investor_id INTEGER,
    transaction_type VARCHAR(20),
    amount REAL NOT NULL,
    state VARCHAR(50),
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Fact: Scheme Performance
CREATE TABLE fact_performance (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id)
);

-- Fact: AUM
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    date_id INTEGER,
    aum_value REAL,
    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);