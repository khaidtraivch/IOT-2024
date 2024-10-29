// Khởi tạo trạng thái thanh toán
let paymentStatus = false;

// Xử lý thanh toán
document.getElementById('bookingForm').addEventListener('submit', function(event) {
    event.preventDefault();
    paymentStatus = true;
    alert("Thanh toán thành công. Bạn đã đặt chỗ!");
});

// Giả lập quét thẻ RFID
function simulateRFIDScan() {
    if (paymentStatus) {
        document.getElementById("rfidMessage").innerText = "Xác thực RFID thành công! Cổng đang mở...";
        // Tích hợp API phần cứng mở cổng tại đây (nếu có)
    } else {
        document.getElementById("rfidMessage").innerText = "Vui lòng thanh toán trước khi quét thẻ RFID.";
    }
}
