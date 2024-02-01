<?php

// Still under development
session_start();
ini_set("display_errors", 0);
include "../connection.php";


if($_SESSION['id_level'] != 1){

    $_SESSION['danger'] = " You not have access to visit that page";
    header("Location: ../login/login.php");

}

$id = mysqli_real_escape_string($conn, $_GET['id']);
$data = mysqli_query($conn, "SELECT * FROM item WHERE id = $id");
$result = mysqli_fetch_array($data);

//var_dump($result);
if(isset($result['id'])){
    http_response_code(404);
}


?>