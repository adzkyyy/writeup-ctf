<?php

$sv = "db";
$db = "hackshop";
$un = "hackshop";
$pw = 1902;
$conn = mysqli_connect($sv,$un,$pw,$db);
mysqli_select_db($conn, $db);
if($conn){
    
} else {
    echo "Failed to Connect to mysql";
}
?>