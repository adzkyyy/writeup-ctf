<?php

include "../header.php";

$p_token = mysqli_real_escape_string($conn, $_REQUEST['token']);
$password = mysqli_real_escape_string($conn, $_REQUEST['password']);

if(isset($p_token, $password) and ctype_alnum($p_token) and $password !== ''){

    $data = mysqli_query($conn, "SELECT * FROM user");
    $tokens = [];
    while($result = mysqli_fetch_array($data)){

        array_push($tokens, $result['token']);

    }

    if(in_array($p_token, $tokens)){

        $hash = md5($password);
        $x = mysqli_query($conn, "UPDATE user SET password = '$hash' WHERE token = '$p_token'");
        $y = mysqli_query($conn, "UPDATE user SET token = '' WHERE token = '$p_token'");

        if($x and $y){
            $_SESSION['status']=" Password Changed";
        }else{
            $_SESSION['danger']=" Failed to change password";
        }
        
        header("Location: ../login/login.php");
        die();

    }else{

        $_SESSION['danger'] = " Invalid password reset link.";
        header("Location: ../login/resetPassword.php");
        die();

    }

}else{

    $_SESSION['danger'] = " Invalid Token Provided.";
    header("Location: ../login/login.php");

}

?>