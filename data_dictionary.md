# Bluestock Mutual Fund Analytics: Data Dictionary

## Dimension Tables

### `dim_fund`
| Column Name   | Data Type    | Description                                      | Source Reference |
|---------------|--------------|--------------------------------------------------|------------------|
| `fund_id`     | INTEGER (PK) | Surrogate key for the fund.                      | System Generated |
| `amfi_code`   | VARCHAR(10)  | Official 6-digit AMFI scheme code.               | fund_master.csv  |
| `scheme_name` | VARCHAR(255) | Full name of the mutual fund scheme.             | fund_master.csv  |
| `fund_house`  | VARCHAR(100) | AMC managing the fund (e.g., HDFC, SBI).         | fund_master.csv  |
| `category`    | VARCHAR(50)  | Broad asset class (Equity, Debt, Hybrid).        | fund_master.csv  |
| `risk_grade`  | VARCHAR(20)  | Risk level (Low, Moderate, High, Very High).     | fund_master.csv  |

### `dim_date`
| Column Name   | Data Type    | Description                                      | Source Reference |
|---------------|--------------|--------------------------------------------------|------------------|
| `date_id`     | INTEGER (PK) | Surrogate key in YYYYMMDD format.                | System Generated |
| `full_date`   | DATE         | Standard ISO date format (YYYY-MM-DD).           | Various CSVs     |
| `is_weekend`  | BOOLEAN      | Flag indicating if the date falls on a weekend.  | Computed         |

## Fact Tables

### `fact_nav`
| Column Name   | Data Type    | Description                                      | Source Reference |
|---------------|--------------|--------------------------------------------------|------------------|
| `nav_id`      | INTEGER (PK) | Surrogate key for the NAV record.                | System Generated |
| `fund_id`     | INTEGER (FK) | Foreign key linking to `dim_fund`.               | nav_history.csv  |
| `date_id`     | INTEGER (FK) | Foreign key linking to `dim_date`.               | nav_history.csv  |
| `nav`         | REAL         | Net Asset Value on the given date (validated >0).| nav_history.csv  |

### `fact_transactions`
| Column Name        | Data Type    | Description                                   | Source Reference |
|--------------------|--------------|-----------------------------------------------|------------------|
| `txn_id`           | INTEGER (PK) | Surrogate key for the transaction.            | System Generated |
| `investor_id`      | INTEGER      | Unique identifier for the client/investor.    | investor_txn.csv |
| `transaction_type` | VARCHAR(20)  | Standardised: 'SIP', 'LUMPSUM', 'REDEMPTION'. | investor_txn.csv |
| `amount`           | REAL         | Monetary value of the transaction (INR).      | investor_txn.csv |

### `fact_performance`
| Column Name      | Data Type    | Description                                     | Source Reference |
|------------------|--------------|-------------------------------------------------|------------------|
| `return_1y`      | REAL         | 1-Year annualized rolling return percentage.    | scheme_perf.csv  |
| `expense_ratio`  | REAL         | Annual expense ratio percentage (0.1 - 2.5).    | scheme_perf.csv  |