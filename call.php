<?php
header("Content-Type:text/html; charset=utf-8");


function ram() {
	$command ="C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe call/ram.py ";
	$output = exec($command);
	print($output);
}
function cpu() {
	$command ="C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe call/cpu.py ";
	$output = exec($command);
	print($output);
}

if (isset($_GET['ram'])) {
	ram();
}
if (isset($_GET['cpu'])) {
	cpu();
}
?>
