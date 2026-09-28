# Spaza Shop Stock Management System

A serverless stock management system designed for small retail stores (spaza shops). I built this system using AWS core services to track inventory, record sales in real time, and automatically flag products that need restocking.

## System Architecture
* **Frontend:** Static HTML/JavaScript interface hosted on **Amazon S3** (or delivered via Amazon CloudFront).
* **API Layer:** **Amazon API Gateway** (HTTP API) routing requests to backend functions.
* **Logic Layer:** **AWS Lambda** (Python 3.x) handling product creation, sales deductions, and restock threshold calculations.
* **Database:** **Amazon DynamoDB** (`SpazaInventory` table) storing product IDs, names, quantities, prices, and restock thresholds.

## Key Features
* **Inventory Tracking:** Allows adding new items or updating existing stock quantities and prices.
* **Sales Recording:** Automatically deducts sold items with conditional checks to prevent negative stock.
* **Restock Alerts:** Filters products reaching or falling below minimum stock thresholds (default: 5 units).
* **Full Inventory Scan:** Retrieves complete stock lists and real-time quantities.

## AWS Deployment Steps
1. **DynamoDB Setup:** Created a table named `SpazaInventory` with `product_id` (String) as the Partition Key.
2. **IAM Policy & Role:** Configured an execution role for Lambda with read/write access to DynamoDB (`dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:GetItem`, `dynamodb:Scan`).
3. **AWS Lambda:** Developed and deployed a Python 3.x function using `lambda_function.py`.
4. **API Gateway Setup:** Configured an HTTP API with CORS enabled and routed the following endpoints to the Lambda function:
   - `POST /product`
   - `POST /sale`
   - `GET /restock`
   - `GET /inventory`
5. **Amazon S3 Hosting:** Uploaded `index.html` to an S3 bucket configured for static website hosting and updated the `API_BASE_URL` in the script tag with the live API Gateway endpoint.
