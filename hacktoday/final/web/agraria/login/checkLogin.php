<?php 
session_start();
include '../connection.php';
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, md5($_POST['password']));

$login = mysqli_query($conn,"SELECT * FROM user WHERE username='$username' AND password='$password'");
$check = mysqli_num_rows($login);

if($check > 0){
	$data = mysqli_fetch_assoc($login);

	if($data['id_level']==1){
        $_SESSION['id'] = $data['id'];
		$_SESSION['username'] = $username;
		$_SESSION['id_level'] = 1;
		$_SESSION['status']=" Log-in";
		header("location: ../users/index.php");
		die();
	}else{
		echo "ID level not found";
    }
}else{
	$_SESSION['danger']=" Username/Password is not correct";
	header("Location: login.php");
}
?>