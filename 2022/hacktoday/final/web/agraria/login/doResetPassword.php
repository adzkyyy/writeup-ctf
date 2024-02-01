<?php

include "../header.php";

$p_token = $_GET['token'];

$data = mysqli_query($conn, "SELECT * FROM user");
$tokens = [];
while($result = mysqli_fetch_array($data)){
    array_push($tokens, $result['token']);
}

if(ctype_alnum($p_token) AND in_array($p_token, $tokens)){

?>

<div class="container">
        <div class="alert alert-success">    
            <strong>Success! </strong> Valid Token Provided, you can change your password below <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="col-md-3">

        </div>
        <div class="container d-flex justify-content-center align-items-center" style="min-height: 50vh">
            <form action="doChangePassword.php" method="POST" class="border shadow p-5 rounded">
                <div class="panel panel-primary">
                    <div class="panel-heading">
                        <center><h1>Change Your Password</h1></center>
                    </div>
                    <div class="panel-body">
                        <input type="hidden" name="token" value="<?php echo htmlentities($p_token); ?>">
                        <div class="form-group">
                            <br>
                            <p class="badge bg-info text-wrap text-dark">note : Password field must contain 8 or more characters consisting of at least<br>one number, one upper and lower case letter, and one special character.</p>
                            <br>
                            <label class="form-label" for="password">New Password :</label>
                            <!--regex-->
                            <!-- Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character -->
                            <div class="col-ls-10">
                                <input type="password" name="password" class="form-control" id="password" placeholder="Enter password" pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$">
                            </div>
                        </div>
                        <br>
                        <input type="submit" value="Change Password" class="btn btn-primary">
                    </div>
                </div>
            </form>
        </div>
        <div class="col-md-3">
            
        </div>
    </div>

<?php 

}else{

    $_SESSION['danger'] = " Invalid password reset link.";
    header("Location: resetPassword.php");
    die();

}




?>