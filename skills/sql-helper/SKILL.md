---
name: sql-helper
description: Help write and optimize SQL queries. Use when user needs to write SQL, debug queries, or understand database operations.
---

# SQL Helper

## Overview

Assists with writing, debugging, and optimizing SQL queries for various database systems.

## When to Use

- User needs to write a SQL query
- User has a query that's not working
- User wants to optimize query performance
- User needs to understand what a query does

## Query Building Process

1. **Understand the goal** - What data do you need?
2. **Identify tables** - Where does the data live?
3. **Define joins** - How are tables related?
4. **Add filters** - What conditions apply?
5. **Select columns** - What fields to return?
6. **Order/Group** - How to organize results?

## Common Query Patterns

### Basic Select
```sql
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1;
```

### Join Tables
```sql
SELECT a.name, b.order_date, b.amount
FROM customers a
JOIN orders b ON a.id = b.customer_id
WHERE b.order_date > '2024-01-01';
```

### Aggregate with Group By
```sql
SELECT category,
       COUNT(*) as count,
       SUM(amount) as total,
       AVG(amount) as average
FROM sales
GROUP BY category
HAVING SUM(amount) > 1000
ORDER BY total DESC;
```

### Subquery
```sql
SELECT *
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

### CTE (Common Table Expression)
```sql
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', date) as month,
           SUM(amount) as total
    FROM sales
    GROUP BY 1
)
SELECT * FROM monthly_sales
WHERE total > 10000;
```

### Window Functions
```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```

## Optimization Tips

1. **Use indexes** on filtered/joined columns
2. **Avoid SELECT *** - specify needed columns
3. **Limit results** during development
4. **Use EXPLAIN** to analyze query plans
5. **Filter early** - reduce data before joins

## Dialect Differences

| Feature | PostgreSQL | MySQL | SQLite |
|---------|------------|-------|--------|
| String concat | `\|\|` | `CONCAT()` | `\|\|` |
| Limit | `LIMIT n` | `LIMIT n` | `LIMIT n` |
| Current time | `NOW()` | `NOW()` | `datetime('now')` |
