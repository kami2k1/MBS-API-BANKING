<?php
header('Content-Type: text/html; charset=utf-8');

// Nếu có yêu cầu kiểm tra trạng thái, thực hiện kiểm tra
if (isset($_GET['check_status']) && $_GET['check_status'] == 'true') {
    $amount = isset($_GET['sotien']) ? $_GET['sotien'] : '0';
    $addInfo = isset($_GET['data']) ? $_GET['data'] : '0';
    if ($addInfo == '0' || $amount == '0' ){
        echo json_encode(['result' => 'failure', 'message' => 'Dữ liệu Đầu Vào bị Sai ']);
        echo   " $amount  $addInfo "  ;

        exit;
    }
    $url = "http://127.0.0.1:4000/?key=kami&adu=$addInfo&t=$amount";
    $maxDuration = 15 * 60; // 15 phút = 900 giây
    $interval = 10;
    $startTime = time();

    while ((time() - $startTime) < $maxDuration) {
        // Khởi tạo cURL
      try{
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10); // Thời gian timeout cURL
        $response = curl_exec($ch);
        curl_close($ch);

        // Kiểm tra mã phản hồi
        if ($response !== false) {
            $data = json_decode($response, true);

            // Nếu phản hồi có 'status' và nó bằng 2
            if (isset($data['status']) && $data['status'] == 2) {
                echo json_encode(['result' => 'success', 'message' => 'Thanh toán thành công']);
                exit;
            }
            if (isset($data['status']) && $data['status'] == 3) {
                echo json_encode(['result' => 'failure', 'message' => 'Thanh toán thất bại Chuyển tiền Không Đủ']);
                exit;
            }
        }

        // Chờ một khoảng thời gian trước khi kiểm tra lại
        sleep($interval);
    }catch (Exception $e){
        continue;
    }
    }

    // Nếu hết thời gian kiểm tra mà không có kết quả thành công
    echo json_encode(['result' => 'failure', 'message' => 'Thanh toán thất bại']);
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR MSb</title>
    <style>
        /* CSS từ phần trên */
        body {
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    margin: 0;
    background-color: #f4f4f4;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

input, button {
    margin: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    background-color: #007bff;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

#qr-code {
    margin-top: 20px;
}

#countdown {
    margin-top: 20px;
    font-size: 18px;
    font-weight: bold;
    color: #333;
}

#status {
    margin-top: 20px;
    font-size: 18px;
    font-weight: bold;
}

.success {
    color: green;
}

.failure {
    color: red;
}

.overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.popup {
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.popup h2 {
    margin: 0;
    font-size: 24px;
}

.popup p {
    margin: 10px 0;
    font-size: 18px;
}

.popup button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 4px;
}

.popup button:hover {
    background-color: #0056b3;
}

    </style>
</head>
<body>
    <h1>Tạo QR Chuyển Khoản MSB</h1>
    <form id="qr-form">
        <label for="amount">Nhập số tiền:</label>
        <input type="number" id="amount" name="amount" required>
        <label for="addInfo">Nhập thông tin thêm:</label>
        <input type="text" id="addInfo" name="addInfo" required>
        <!-- <label for="accountName">Nhập tên tài khoản:</label>
        <input type="text" id="accountName" name="accountName" required> -->
        <button type="submit">Tạo QR</button>
    </form>
    <div id="qr-code"></div>
    <div id="countdown"></div>
    <div id="status"></div>

    <!-- Popup và lớp phủ -->
    <div id="overlay" class="overlay">
        <div class="popup">
            <h2>Thanh toán thành công!</h2>
            <p>QR Code đã được tạo và thanh toán đã hoàn tất.</p>
            <button id="close-popup">Đóng</button>
        </div>
    </div>

    <script>
        document.getElementById('qr-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const amount = document.getElementById('amount').value;
            const addInfo = document.getElementById('addInfo').value;
            // const accountName = document.getElementById('accountName').value;
            const qrCodeContainer = document.getElementById('qr-code');
            const statusContainer = document.getElementById('status');
            const countdownContainer = document.getElementById('countdown');
            qrCodeContainer.innerHTML = ''; // Xóa nội dung QR code cũ
            statusContainer.innerHTML = ''; // Xóa nội dung trạng thái cũ
            countdownContainer.innerHTML = ''; // Xóa đồng hồ đếm ngược cũ

            // Build the URL for the QR code image
            const baseUrl = "https://img.vietqr.io/image/MSB-quangdev-compact2.jpg";
            const params = new URLSearchParams({
                amount: amount,
                addInfo: addInfo,
                accountName: "Dang Hung Quang"
            });
            
            const qrUrl = `${baseUrl}?${params.toString()}`;

            // Create an img element and set its src attribute to the QR code URL
            const img = document.createElement('img');
            img.src = qrUrl;
            img.alt = 'QR Code';
            qrCodeContainer.appendChild(img);

            // Gửi yêu cầu kiểm tra trạng thái
            let countdownEnd = Date.now() + (15 * 60 * 1000); // 15 phút sau
            let countdownInterval;

            function checkPaymentStatus() {
                fetch('?check_status=true&sotien='+amount +"&data="+addInfo)
                    .then(response => response.json())
                    .then(data => {
                        if (data.result === 'success') {
                            statusContainer.textContent = data.message;
                            statusContainer.className = 'success';
                            showPopup(); // Hiển thị popup khi thanh toán thành công
                            clearInterval(countdownInterval); // Dừng đồng hồ đếm ngược
                        } else {
                            statusContainer.textContent = data.message;
                            statusContainer.className = 'failure';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        statusContainer.textContent =  data.message;
                        statusContainer.className = 'failure';
                    });
            }

            function updateCountdown() {
                const now = Date.now();
                const timeLeft = countdownEnd - now;

                if (timeLeft <= 0) {
                    countdownContainer.textContent = 'Thời gian thanh toán đã hết.';
                    return;
                }

                const minutes = Math.floor((timeLeft / 1000 / 60) % 60);
                const seconds = Math.floor((timeLeft / 1000) % 60);
                countdownContainer.textContent = `Thời gian còn lại: ${minutes} phút ${seconds} giây`;
            }

            function showPopup() {
                document.getElementById('overlay').style.display = 'flex';
            }

            function closePopup() {
                document.getElementById('overlay').style.display = 'none';
            }

            // Bắt đầu kiểm tra trạng thái và đồng hồ đếm ngược
            checkPaymentStatus();
            countdownInterval = setInterval(updateCountdown, 1000); // Cập nhật đồng hồ đếm ngược mỗi giây

            // Gán sự kiện đóng popup
            document.getElementById('close-popup').addEventListener('click', closePopup);
        });
    </script>
</body>
</html>
