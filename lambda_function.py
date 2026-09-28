import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SpazaInventory')

# Helper function to serialize Decimal objects from DynamoDB
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    path = event.get('rawPath', event.get('path', ''))
    method = event.get('requestContext', {}).get('http', {}).get('method', event.get('httpMethod', ''))
    
    # 1. Add or Update a Product
    if method == 'POST' and '/product' in path:
        body = json.loads(event.get('body', '{}'))
        table.put_item(
            Item={
                'product_id': body['product_id'],
                'product_name': body['product_name'],
                'quantity': int(body['quantity']),
                'price': Decimal(str(body['price'])),
                'restock_threshold': int(body.get('restock_threshold', 5))
            }
        )
        return response(200, {'message': f"Product {body['product_name']} added/updated successfully."})

    # 2. Record a Sale
    elif method == 'POST' and '/sale' in path:
        body = json.loads(event.get('body', '{}'))
        product_id = body['product_id']
        qty_sold = int(body['quantity_sold'])
        
        try:
            # Decrement stock safely if sufficient quantity exists
            table.update_item(
                Key={'product_id': product_id},
                UpdateExpression="SET quantity = quantity - :val",
                ConditionExpression="quantity >= :val",
                ExpressionAttributeValues={':val': qty_sold}
            )
            return response(200, {'message': f"Sale recorded for product {product_id}."})
        except boto3.client('dynamodb').exceptions.ConditionalCheckFailedException:
            return response(400, {'error': 'Insufficient stock available.'})

    # 3. Get Restock Alert List
    elif method == 'GET' and '/restock' in path:
        response_data = table.scan()
        items = response_data.get('Items', [])
        
        # Filter products where quantity is at or below threshold
        restock_list = [
            item for item in items 
            if item.get('quantity', 0) <= item.get('restock_threshold', 5)
        ]
        return response(200, {'restock_needed': restock_list})

    # 4. View Full Inventory
    elif method == 'GET' and '/inventory' in path:
        response_data = table.scan()
        return response(200, {'inventory': response_data.get('Items', [])})

    return response(404, {'error': 'Route not found'})


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Enable CORS for web frontend
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }