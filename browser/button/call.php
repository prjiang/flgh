<?php

/*
function ram() {
	$command = "C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe call/ram.py";
	$output = exec($command);
	echo($output);
}
*/
function ram() {	
	$command = "tasklist /fo list";
	$output = shell_exec($command);
	$result = str_replace("\n","<br>",$output);
	echo iconv("big5","UTF-8//IGNORE", $result);	
}
function cpu() {
	$command = "C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe call/cpu.py ";
	$output = exec($command);
	echo($output);
}


if (isset($_GET['ram'])) {
	ram();
}
if (isset($_GET['cpu'])) {
	cpu();
}
?>
