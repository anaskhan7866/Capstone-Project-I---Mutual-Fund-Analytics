-- 1. Top 5 funds by latest AUM
SELECT f.scheme_name, a.aum_value 
FROM fact_aum a
JOIN dim_fund f ON a.fund_id = f.fund_id
ORDER BY a.aum_value DESC 
LIMIT 5;

-- 2. Average NAV per month for a specific fund
SELECT d.year, d.month, f.scheme_name, AVG(n.nav) as avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date_id = d.date_id
JOIN dim_fund f ON n.fund_id = f.fund_id
GROUP BY d.year, d.month, f.scheme_name;

-- 3. SIP Year-over-Year (YoY) Growth Volume
SELECT d.year, SUM(t.amount) as total_sip_volume
FROM fact_transactions t
JOIN dim_date d ON t.date_id = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year ASC;

-- 4. Total Transaction Volume by State
SELECT state, transaction_type, SUM(amount) as total_volume
FROM fact_transactions
GROUP BY state, transaction_type
ORDER BY total_volume DESC;

-- 5. Funds with expense_ratio < 1%
SELECT f.scheme_name, p.expense_ratio, f.category
FROM fact_performance p
JOIN dim_fund f ON p.fund_id = f.fund_id
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. Top 3 performing funds in 3-Year returns
SELECT f.scheme_name, p.return_3y, f.fund_house
FROM fact_performance p
JOIN dim_fund f ON p.fund_id = f.fund_id
ORDER BY p.return_3y DESC
LIMIT 3;

-- 7. Monthly Redemption vs Lumpsum volume ratio
SELECT d.year, d.month,
       SUM(CASE WHEN t.transaction_type = 'REDEMPTION' THEN t.amount ELSE 0 END) as total_redemption,
       SUM(CASE WHEN t.transaction_type = 'LUMPSUM' THEN t.amount ELSE 0 END) as total_lumpsum
FROM fact_transactions t
JOIN dim_date d ON t.date_id = d.date_id
GROUP BY d.year, d.month;

-- 8. Average AUM of High-Risk Grade Funds
SELECT f.risk_grade, AVG(a.aum_value) as avg_aum
FROM dim_fund f
JOIN fact_aum a ON f.fund_id = a.fund_id
WHERE f.risk_grade = 'High' OR f.risk_grade = 'Very High'
GROUP BY f.risk_grade;

-- 9. Active Funds Count per Fund House
SELECT fund_house, COUNT(DISTINCT fund_id) as active_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY active_schemes DESC;

-- 10. Top 5 Investors by Total Investment (SIP + LUMPSUM)
SELECT investor_id, SUM(amount) as total_invested
FROM fact_transactions
WHERE transaction_type IN ('SIP', 'LUMPSUM')
GROUP BY investor_id
ORDER BY total_invested DESC
LIMIT 5;