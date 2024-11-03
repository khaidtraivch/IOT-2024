<script>
    let ws;

    // Khởi tạo WebSocket và thiết lập các sự kiện
    function initWebSocket() {
        ws = new WebSocket('ws://localhost:8765'); // Thay bằng IP server nếu cần

        // Sự kiện mở kết nối WebSocket
        ws.onopen = function() {
            console.log('Connected to WebSocket server');
            document.getElementById('slotStatus').innerText = "Connected to server.";
        };

        // Xử lý tin nhắn từ server
        ws.onmessage = function(event) {
            const message = JSON.parse(event.data);

            if (message.type === 'parkingStatus') {
                // Cập nhật trạng thái chỗ đỗ xe
                document.getElementById('slotStatus').innerText = `Slot ${message.slot}: ${message.status}`;
            } else if (message.type === 'rfidStatus') {
                // Hiển thị trạng thái RFID
                document.getElementById('rfidMessage').innerText = message.message;
            } else if (message.type === 'bookingConfirmation') {
                // Hiển thị xác nhận đặt chỗ
                document.getElementById('slotStatus').innerText = `Booking confirmed for Slot ${message.slot} from ${message.startTime} to ${message.endTime}`;
            } else if (message.type === 'error') {
                // Xử lý và hiển thị lỗi từ server
                console.error("Error from server:", message.message);
                document.getElementById('slotStatus').innerText = `Error: ${message.message}`;
            }
        };

        // Xử lý ngắt kết nối WebSocket
        ws.onclose = function() {
            console.log('Disconnected from WebSocket server');
            document.getElementById('slotStatus').innerText = "Disconnected from server. Attempting to reconnect...";

            // Thử kết nối lại sau 3 giây nếu bị ngắt
            setTimeout(() => {
                document.getElementById('slotStatus').innerText = "Reconnecting...";
                reconnectWebSocket();
            }, 3000);
        };

        // Xử lý lỗi kết nối WebSocket
        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }

    // Hàm kết nối lại WebSocket
    function reconnectWebSocket() {
        if (ws.readyState !== WebSocket.OPEN && ws.readyState !== WebSocket.CONNECTING) {
            initWebSocket();
        }
    }

    // Gửi dữ liệu WebSocket với kiểm tra kết nối
    function sendWebSocketMessage(data) {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(data));
        } else {
            console.error('WebSocket is not open. Message not sent:', data);
            document.getElementById('slotStatus').innerText = "Unable to send message. WebSocket not connected.";
        }
    }

    // Gửi yêu cầu đặt chỗ
    function submitBooking(event) {
        event.preventDefault();
        const slot = document.getElementById('slot').value;
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;

        const bookingData = {
            type: 'booking',
            slot: slot,
            startTime: startTime,
            endTime: endTime
        };

        sendWebSocketMessage(bookingData);
        document.getElementById('slotStatus').innerText = "Booking submitted. Waiting for confirmation...";
    }

    // Gửi yêu cầu quét RFID
    function requestRFIDScan() {
        const rfidRequest = { type: 'rfidScanRequest' };
        sendWebSocketMessage(rfidRequest);
        document.getElementById('rfidMessage').innerText = "Please scan your RFID card...";
    }

    // Gửi yêu cầu cập nhật trạng thái chỗ đỗ
    function updateParkingStatus(slot, status) {
        const statusUpdate = {
            type: 'update_status',
            slot: slot,
            status: status
        };

        sendWebSocketMessage(statusUpdate);
        document.getElementById('slotStatus').innerText = `Updating status for Slot ${slot} to ${status}...`;
    }

    // Khởi tạo WebSocket khi tải trang
    window.onload = function() {
        initWebSocket();
    };
</script>
