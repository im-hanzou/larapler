<?php
// Speciment ID
// Fixed by im-hanzou
// With auto delete duplicate line
// Usage : php laravel.php

function checker($url, $file){

$headers = array();
$headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0';
$headers[] = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8';
$headers[] = 'Accept-Language: en-US,en;q=0.5';
$headers[] = 'Content-Type: application/x-www-form-urlencoded';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_HEADER, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$header = substr($response, 0, $header_size);
$body = substr($response, $header_size);
curl_close($ch);

    preg_match_all('/^Set-Cookie:\s*([^;]*)/mi', $header, $outCookie);
    $cookies = '';
    
    foreach($outCookie[1] as $outCookies) {
        $cookies .= $outCookies.'; ';
    }
    
    if(preg_match_all("/_session/", $cookies)){
	    $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
	    if (!in_array($url, $lines)) {
	    file_put_contents($file, $url . PHP_EOL, FILE_APPEND | LOCK_EX);
	    }
	    return json_encode(array("laravel" => TRUE));

    }if(preg_match_all("/XSRF-TOKEN/", $cookies)){
	    $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
	    if (!in_array($url, $lines)) {
	    file_put_contents($file, $url . PHP_EOL, FILE_APPEND | LOCK_EX);
	    }
	    return json_encode(array("laravel" => TRUE));

    }else{
	    $lines = file('invalid_laravel.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
	    if (!in_array($url, $lines)) {
		    file_put_contents('invalid_laravel.txt', $url . PHP_EOL, FILE_APPEND | LOCK_EX);
	    }
	    return json_encode(array("laravel" => FALSE));
    }
}

echo "Laravel Checker".PHP_EOL;
echo "Created By : Speciment ID".PHP_EOL;
echo PHP_EOL;
echo "Input List : ";
$list = file_get_contents(trim(fgets(STDIN)));
echo "Output : ";
$output = trim(fgets(STDIN));
if (!file_exists($output)) {
    touch($output);
}
$exp = explode(PHP_EOL, trim($list));

$i = 1;
foreach($exp as $site){
	echo $i.". ".$site." : ".checker($site, $output).PHP_EOL;
	$i++;
}
