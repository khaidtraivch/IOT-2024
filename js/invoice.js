let invoices = [];

// Thêm hóa đơn mới
function addInvoice() {
    const invoiceId = document.getElementById('invoiceId').value;
    const customerName = document.getElementById('customerName').value;
    const amount = document.getElementById('amount').value;

    if (!invoiceId || !customerName || !amount) {
        alert("Vui lòng điền đầy đủ thông tin.");
        return;
    }

    const newInvoice = { invoiceId, customerName, amount };
    invoices.push(newInvoice);
    renderInvoices();
    clearForm();
}

// Hiển thị danh sách hóa đơn
function renderInvoices() {
    const invoiceTable = document.getElementById('invoiceTable').getElementsByTagName('tbody')[0];
    invoiceTable.innerHTML = ''; // Xóa nội dung cũ

    invoices.forEach((invoice, index) => {
        const row = invoiceTable.insertRow();
        
        row.insertCell(0).innerText = invoice.invoiceId;
        row.insertCell(1).innerText = invoice.customerName;
        row.insertCell(2).innerText = invoice.amount;

        // Tạo các nút chỉnh sửa và xóa
        const actionCell = row.insertCell(3);
        actionCell.innerHTML = `
            <button onclick="editInvoice(${index})">Sửa</button>
            <button onclick="deleteInvoice(${index})">Xóa</button>
        `;
    });
}

// Xóa hóa đơn
function deleteInvoice(index) {
    invoices.splice(index, 1);
    renderInvoices();
}

// Sửa hóa đơn
function editInvoice(index) {
    const invoice = invoices[index];
    document.getElementById('invoiceId').value = invoice.invoiceId;
    document.getElementById('customerName').value = invoice.customerName;
    document.getElementById('amount').value = invoice.amount;

    // Cập nhật nút thêm thành nút lưu
    const submitButton = document.querySelector('#invoiceForm button');
    submitButton.textContent = 'Lưu thay đổi';
    submitButton.onclick = function () {
        saveInvoice(index);
    };
}

// Lưu thay đổi hóa đơn
function saveInvoice(index) {
    invoices[index].invoiceId = document.getElementById('invoiceId').value;
    invoices[index].customerName = document.getElementById('customerName').value;
    invoices[index].amount = document.getElementById('amount').value;

    renderInvoices();
    clearForm();

    // Đổi lại nút lưu thành nút thêm
    const submitButton = document.querySelector('#invoiceForm button');
    submitButton.textContent = 'Thêm hóa đơn';
    submitButton.onclick = addInvoice;
}

// Xóa các ô nhập liệu sau khi hoàn tất
function clearForm() {
    document.getElementById('invoiceId').value = '';
    document.getElementById('customerName').value = '';
    document.getElementById('amount').value = '';
}
