<?php
// Pythonスクリプトを実行

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST["foecast_info_update1"])) {
        $arg = '1';
    } elseif (isset($_POST["button2"])) {
        $arg = 2;
    } elseif (isset($_POST["button3"])) {
        $arg = 3;
    } else {
        $arg = 0; 
    }
    // exec("python3 /path/to/your/webserver/forecast.py $arg");

    // Pythonスクリプトを実行
    $command = 'python3 update_image.py ' . escapeshellarg($arg);
    $output = shell_exec($command);
    // 画像を更新するためにHTMLページにリダイレクト
    header('Location: forecast_info.html');
}

?>

