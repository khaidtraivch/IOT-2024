import asyncio
import websockets
import json
from datetime import datetime

# Server address and port
SERVER_HOST = '0.0.0.0'  # Listening on all IPs on the server
SERVER_PORT = 8765

# Connected clients for broadcasting data
clients = set()

# Invoice data and parking slot status
invoices = []
parking_spots = {"1": "available", "2": "available", "3": "available", "4": "available"}

# List of authorized RFID IDs
authorized_ids = {
    "123456789": "Alice",
    "987654321": "Bob",
}

# Pricing information
pricing_per_hour = 5.0  # Define hourly rate in your local currency

# Function to broadcast data to all clients
async def broadcast(data):
    if clients:
        message = json.dumps(data)
        await asyncio.wait([asyncio.create_task(client.send(message)) for client in clients])

# WebSocket connection handler
async def handle_connection(websocket, path):
    print("New connection established")
    clients.add(websocket)

    try:
        # Send initial data about parking status and invoices
        await websocket.send(json.dumps({"type": "parkingStatus", "spots": parking_spots}))
        await websocket.send(json.dumps({"type": "invoiceList", "invoices": invoices}))

        async for message in websocket:
            print(f"Received message: {message}")
            data = json.loads(message)

            # Handle booking request
            if data['type'] == 'booking':
                slot = data['slot']
                start_time = datetime.fromisoformat(data['startTime'])
                end_time = datetime.fromisoformat(data['endTime'])
                
                # Check parking slot availability
                if parking_spots[slot] == "available":
                    # Calculate total cost
                    duration_hours = (end_time - start_time).total_seconds() / 3600
                    total_cost = round(duration_hours * pricing_per_hour, 2)
                    
                    # Simulate payment processing (you would integrate an actual payment gateway here)
                    payment_status = "successful"  # Simulate a successful payment

                    if payment_status == "successful":
                        parking_spots[slot] = "occupied"  # Set slot status to "occupied"
                        
                        # Generate invoice and store
                        invoice = {
                            "slot": slot,
                            "startTime": data['startTime'],
                            "endTime": data['endTime'],
                            "cost": total_cost,
                            "status": "paid"
                        }
                        invoices.append(invoice)

                        # Send booking confirmation to the user
                        response = {
                            "type": "bookingConfirmation",
                            "slot": slot,
                            "startTime": data['startTime'],
                            "endTime": data['endTime'],
                            "cost": total_cost,
                            "status": "confirmed",
                            "rfidAccessGranted": True  # Grant RFID access
                        }
                        await websocket.send(json.dumps(response))
                        
                        # Broadcast parking status update to all clients
                        await broadcast({"type": "parkingStatus", "slot": slot, "status": "occupied"})
                        print(f"Booking confirmed and payment processed for Slot {slot}")
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": "Payment failed. Please try again."
                        }))
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Slot {slot} is already occupied."
                    }))

            elif data['type'] == 'rfidScanRequest':
                rfid_id = "123456789"  # Simulate received RFID ID
                user = authorized_ids.get(rfid_id)
                
                if user:
                    response = {
                        "type": "rfidStatus",
                        "message": f"Welcome, {user}! Access granted.",
                        "status": "Door opened"
                    }
                else:
                    response = {
                        "type": "rfidStatus",
                        "message": "Access denied. Unauthorized RFID card.",
                        "status": "Door closed"
                    }
                
                await websocket.send(json.dumps(response))
                print("RFID scan processed")

            elif data['type'] == 'update_status':
                slot = data['slot']
                status = data['status']
                parking_spots[slot] = status
                await broadcast({"type": "parkingStatus", "slot": slot, "status": status})
                print(f"Parking slot {slot} updated to {status}")

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)
        print("Connection removed")

# WebSocket server main entry point
async def main():
    async with websockets.serve(handle_connection, SERVER_HOST, SERVER_PORT):
        print(f"WebSocket server running on ws://{SERVER_HOST}:{SERVER_PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Server encountered an error: {e}")
