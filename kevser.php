<?php
date_default_timezone_set('Europe/Istanbul');

// GET parametrelerini al
$sicaklik = isset($_GET['sicaklik']) ? $_GET['sicaklik'] : null;
$nem = isset($_GET['nem']) ? $_GET['nem'] : null;

// Veri doğrulama ve filtreleme
if ($sicaklik !== null && $nem !== null) {

    // Sadece sayı ve ondalık karakterleri kabul et
    if (preg_match('/^\d+(\.\d+)?$/', $sicaklik) && preg_match('/^\d+(\.\d+)?$/', $nem)) {

        $zaman = date("Y-m-d H:i:s");
        $satir = "[$zaman] Sicaklik: $sicaklik °C | Nem: $nem %\n";

        // Veriyi log dosyasına yaz
        file_put_contents("kevser.txt", $satir, FILE_APPEND | LOCK_EX);

        echo "Veri alindi: $satir";

    } else {
        // Eğer sayı değilse giriş reddedilir
        echo "Hatali veri formati!";
    }

} else {
    echo "Hatalı istek: sicaklik ve/veya nem parametreleri eksik.";
}
?>
