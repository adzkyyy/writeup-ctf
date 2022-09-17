<?php
session_start();
include "../connection.php";
$username = mysqli_real_escape_string($conn, @$_POST['username']);

if(isset($username) and ctype_alnum($username)){

    $data = mysqli_query($conn, "SELECT * FROM user");
    $users = [];
    while($result= mysqli_fetch_array($data)){
        array_push($users, $result['username']);
    }

    if(in_array($username, $users)){

        $token = generateToken();
        mysqli_query($conn,"UPDATE user SET token = '$token' WHERE username = '$username'");
        send_email($username, $token);
        $_SESSION['status']=" Password Reset token has been generated";    
        header("location: login.php");
        die();

    }else{

        $_SESSION['danger']=" Username not found.";
        header("location: pageReset.php");
        die();

    }
}



function generateToken(){
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < 15; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

function send_email($username, $token){
    
    $message = "Hello ".htmlentities($username).",\n";
    $message .= "Please follow the link below to reset your password: \n";
    $message .= "http://".gethostname()."/doResetPassword.php?token=$token \n";
    $message .= "Thanks.\n";
    global $conn;
    $data = mysqli_query($conn, "SELECT * FROM user WHERE username='$username'");
    while($result= mysqli_fetch_array($data)){
        $email = $result['email'];
    }
    @mail($email, "Reset Your Password", $message);

}

?>