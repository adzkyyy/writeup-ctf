<?php

if($sil!=1){
    $_SESSION['danger']="You not have access to visit that page";
    header("Location: ../index.php");
    die();
}

?>