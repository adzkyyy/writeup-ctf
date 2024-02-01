<?php 
include "../header.php";
?>

</head>
<body>  
<div class="container d-flex justify-content-center align-items-center" style="min-height: 75vh">
    <form action="resetPassword.php" method="POST" class="border shadow p-5 rounded">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <center><h2>Reset your Password</h2></center>
            </div>
            <div class="panel-body">
                <div class="form-group">
                    <label class="form-label" for="username">Username :</label>
                    <input type="text" name="username" class="form-control" id="username" placeholder="Username">
                </div>
                <br>
                <input type="submit" value="Submit" class="btn btn-primary">
            </div>
        </div>
    </form>
</div>
</body>
</html>
