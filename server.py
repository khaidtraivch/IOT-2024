import asyncio
import websockets
import json
from datetime import datetime

# Địa chỉ và cổng server
SERVER_HOST = '0.0.0.0'  # Lắng nghe tất cả các IP trên máy chủ
SERVER_PORT = 8765

# Danh sách các client kết nối để phát dữ liệu
clients = set()

# Dữ liệu hóa đơn và trạng thái chỗ đỗ xe
invoices = []
parking_spots = {"1": "available", "2": "available", "3": "available", "4": "available"}

# Danh sách ID RFID hợp lệ
authorized_ids = {
    "123456789": "Alice",
    "987654321": "Bob",
}

# Hàm phát dữ liệu đến tất cả client
async def broadcast(data):
    if clients:
        message = json.dumps(data)
        # Sử dụng asyncio.create_task để tạo các task từ coroutine
        await asyncio.wait([asyncio.create_task(client.send(message)) for client in clients])

# Hàm xử lý kết nối WebSocket
async def handle_connection(websocket, path):
    print("New connection established")
    clients.add(websocket)

    try:
        # Gửi dữ liệu ban đầu về trạng thái bãi đỗ và hóa đơn
        await websocket.send(json.dumps({"type": "parkingStatus", "spots": parking_spots}))
        await websocket.send(json.dumps({"type": "invoiceList", "invoices": invoices}))

        async for message in websocket:
            print(f"Received message: {message}")
            data = json.loads(message)

            # Xử lý các loại yêu cầu từ client
            if data['type'] == 'booking':
                slot = data['slot']
                start_time = data['startTime']
                end_time = data['endTime']
                
                # Kiểm tra trạng thái chỗ đỗ trước khi đặt chỗ
                if parking_spots[slot] == "available":
                    parking_spots[slot] = "occupied"  # Đặt trạng thái chỗ đỗ thành "occupied"
                    response = {
                        "type": "bookingConfirmation",
                        "slot": slot,
                        "startTime": start_time,
                        "endTime": end_time,
                        "status": "confirmed"
                    }
                    await websocket.send(json.dumps(response))
                    
                    # Phát lại cập nhật trạng thái chỗ đỗ cho tất cả client
                    await broadcast({"type": "parkingStatus", "slot": slot, "status": "occupied"})
                    print(f"Booking confirmed for Slot {slot}")
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Slot {slot} is already occupied."
                    }))

            elif data['type'] == 'rfidScanRequest':
                rfid_id = "123456789"  # Giả lập RFID ID nhận được
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

# Điểm vào chính của server WebSocket
async def main():
    async with websockets.serve(handle_connection, SERVER_HOST, SERVER_PORT):
        print(f"WebSocket server running on ws://{SERVER_HOST}:{SERVER_PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Server encountered an error: {e}")
