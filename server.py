import asyncio
import websockets
import json

# Define the server IP and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8765

# Maintain a list of connected clients for broadcasting updates
clients = set()

# Store invoice and parking status data
invoices = []
parking_spots = {"1": "available", "2": "available", "3": "available", "4": "available"}

# Function to broadcast data to all connected clients
async def broadcast(data):
    if clients:  # Only attempt broadcast if there are clients
        message = json.dumps(data)
        await asyncio.wait([client.send(message) for client in clients])

# Function to handle WebSocket connections
async def handle_connection(websocket, path):
    print("New connection established")
    clients.add(websocket)  # Add client to the set

    try:
        # Send initial data to the client
        await websocket.send(json.dumps({"type": "parkingStatus", "spots": parking_spots}))
        await websocket.send(json.dumps({"type": "invoiceList", "invoices": invoices}))

        async for message in websocket:
            print(f"Received message: {message}")
            data = json.loads(message)

            # Handle messages based on action
            if data['type'] == 'update_status':
                # ESP32 updates parking spot status
                parking_spots[data['slot']] = data['status']
                await broadcast({"type": "parkingStatus", "spots": parking_spots})

            elif data['type'] == 'rfidScan':
                # Process RFID data and broadcast the result
                user = data.get('user', 'Unknown User')
                await broadcast({"type": "rfidStatus", "message": f"RFID scanned for {user}"})

            elif data['type'] == 'addInvoice':
                # Add a new invoice to the list and broadcast update
                invoices.append(data['invoice'])
                await broadcast({"type": "invoiceAdded", "invoice": data['invoice']})

            elif data['type'] == 'removeInvoice':
                # Remove an invoice by ID and broadcast update
                invoice_id = data['invoiceId']
                invoices[:] = [inv for inv in invoices if inv["id"] != invoice_id]
                await broadcast({"type": "invoiceDeleted", "invoiceId": invoice_id})

            elif data['type'] == 'getInvoices':
                # Send the current invoice list to the requester
                await websocket.send(json.dumps({"type": "invoiceList", "invoices": invoices}))

            print("Data processed and broadcasted")

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)
        print("Connection removed")

# Main entry point for WebSocket server
async def main():
    async with websockets.serve(handle_connection, SERVER_HOST, SERVER_PORT):
        print(f"WebSocket server running on ws://{SERVER_HOST}:{SERVER_PORT}")
        await asyncio.Future()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
