<?php
// header("Content-Type:text/html; charset=utf-8");
/*
$command ="C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe call/ram.py ";
$output = exec($command);
print($output);
*/

/*
	$locale = 'zh_CN.UTF-8';
	setlocale(LC_ALL, $locale);
	putenv('LC_ALL='.$locale);
*/

// taskkill /s  /u  /p  /f /im chrome.exe

if (isset($_POST['submit'])) {
	$ip = $_POST['ip'];
	$user = $_POST['user'];
	$pw = $_POST['pw'];
	$command ="tasklist /s $ip /u $user /p $pw /fo list /V > data\\test.txt";
	echo 'IP: '.$ip.'<br>';
	$output = shell_exec($command);
	$result = str_replace("\n","<br>",$output);
	echo iconv("big5","UTF-8//IGNORE", $result);
}

?>