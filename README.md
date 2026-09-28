# Spaza Shop Stock Management System

A serverless stock management system designed for small retail stores (spaza shops). I built this system using AWS core services to track inventory, record sales in real time, and automatically flag products that need restocking.

## System Architecture
* **Frontend:** Static HTML/JavaScript interface hosted on **Amazon S3** (or delivered via Amazon CloudFront).
* **API Layer:** **Amazon API Gateway** (HTTP API) routing requests to backend functions.
* **Logic Layer:** **AWS Lambda** (Python) handling product creation, sales deductions, and restock threshold calculations.
* **Database:** **Amazon DynamoDB** (`SpazaInventory` table) storing product IDs, names, quantities, prices, and restock thresholds.

## Key Features
* **Inventory Tracking:** Allows adding new items or updating existing stock quantities and prices.
* **Sales Recording:** Automatically deducts sold items with conditional checks to prevent negative stock.
* **Restock Alerts:** Filters products reaching or falling below minimum stock thresholds (default: 5 units).
* **Full Inventory Scan:** Retrieves complete stock lists and real-time quantities.
