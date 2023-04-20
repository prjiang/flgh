<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title><?php 
		if (isset($_POST['submit'])) { 
			echo $_POST['ip'];
		}
	?></title>
</head>

<body>
	<div>
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
	
			$command = "tasklist /s $ip /u $user /p $pw /fo list";
			//$save_command = "tasklist /s $ip /u $user /p $pw /fo list /V > info\\test.txt";
			echo 'IP: '.$ip.'<br>';
			$output = shell_exec($command);
			$result = str_replace("\n","<br>",$output);
			echo iconv("big5","UTF-8//IGNORE", $result);

	
			$filename = "info\\test.txt";
			if(@$fp = fopen($filename, 'w+')) {
				fwrite($fp, $output);
				fclose($fp);
			}

			$tocsv = shell_exec("C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe main.py");


			//$dataset -> ImportFromCSV("info/test.csv",",",array(1),false);

		}

	?>
	</div>
</body>
</html>