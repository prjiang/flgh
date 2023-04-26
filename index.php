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

			//$command = "tasklist /s $ip /u $user /p $pw /fo list 2>&1 1> /dev/null"; 解決內部正常運作，但php讀不到
			$command_list = "tasklist /s $ip /u $user /p $pw /fo list";
			$command_csv = shell_exec("tasklist /s $ip /u $user /p $pw /fo csv");
			//$save_command = "tasklist /s $ip /u $user /p $pw /fo csv > info\\test2.txt";
			//exec($save_command);
			echo '<b style="font-size:20px">IP: '.$ip.'</b><hr>';

			$output = shell_exec($command_list);
			$result = str_replace("\n","<br>",$output);
			//echo iconv("big5","UTF-8//IGNORE", $result);
			
	
			$filename = "info\\test.txt";
			if(@$fp = fopen($filename, 'w+')) {
				fwrite($fp, $command_csv);
				fclose($fp);
			}

			$tocsv = shell_exec("C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe csvprocess.py");
			
			$draw = shell_exec("C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe draw.py");

			echo "\n<img src='info\\ram.png'>"."\n<hr>";

			//echo iconv("big5","UTF-8//IGNORE", $result);

			echo "\n<table>\n\n";
			$file = fopen("info\\test.csv", "r");
			while (($line = fgetcsv($file)) !== false) {
        		echo "<tr>";
        		foreach ($line as $cell) {
                	echo "<td>" . htmlspecialchars($cell) . "</td>";
        		}
        		echo "</tr>\n";
			}
			fclose($file);
			echo "\n</table>";

			/*
			session_start();
			include("pChart/class/pDraw.class.php");
			include("pChart/class/pImage.class.php");
			include("pChart/class/pData.class.php");

			$DataSet = new pData();
			$DataSet -> ImportFromCSV("info/test.csv");
			*/

		}

	?>
	</div>

</body>
</html>