# Spaza Shop Stock Management System

A serverless stock management system designed for small retail stores (spaza shops). Built using AWS core services to track inventory, record sales, and identify products that need restocking.

## 🏗️ System Architecture
* **Frontend:** Static HTML/JavaScript interface hosted on **Amazon S3** (or delivered via Amazon CloudFront).
* **API Layer:** **Amazon API Gateway** (HTTP API) routing requests to backend functions.
* **Logic Layer:** **AWS Lambda** (Python 3.x) managing product creation, sales deductions, and restock calculations.
* **Database:** **Amazon DynamoDB** (`SpazaInventory` table) storing product IDs, names, quantities, prices, and restock thresholds.

## 🚀 Key Features
* **Inventory Tracking:** Add new items or update existing stock quantities and prices.
* **Sales Recording:** Automatically deduct sold items with conditional checks to prevent negative stock.
* **Restock Alerts:** Filter products reaching or falling below minimum stock thresholds (default: 5 units).
* **Full Inventory Scan:** Retrieve complete stock lists and real-time quantities.

## 🛠️ AWS Deployment Guide
1. **DynamoDB:** Create a table named `SpazaInventory` with `product_id` (String) as the Partition Key.
2. **IAM Role:** Create an execution role for Lambda with read/write access to DynamoDB (`dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:GetItem`, `dynamodb:Scan`).
3. **AWS Lambda:** Create a Python 3.x function using `lambda_function.py`.
4. **API Gateway:** Set up an HTTP API with CORS enabled and route the endpoints:
   - `POST /product`
   - `POST /sale`
   - `GET /restock`
   - `GET /inventory`
5. **Amazon S3:** Upload `index.html` to an S3 bucket configured for static website hosting and update the `API_BASE_URL` in the script tag with your API Gateway endpoint.
