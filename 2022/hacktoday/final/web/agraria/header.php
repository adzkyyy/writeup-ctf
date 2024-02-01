<?php
session_start();
ini_set("error_reporting", 0);
include 'connection.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agria Web</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<?php
// session id
if(isset($_SESSION['id'])){
    $sid = $_SESSION['id'];
    $sus = $_SESSION['username'];
    $sil = $_SESSION['id_level'];
    // navigate sil == 1
    if($sil == 1){
        ?>
        <!-- start navbar -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
        <a class="navbar-brand" href="#">Agria Web</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarText">
            <ul class="nav navbar-nav">
            <?php
                if(!isset($_GET['page'])){
                    ?>
                    <li class = "nav-link"><a href="../users/index.php?page=user">Users</a></li>
                    <li class = "nav-link"><a  href="../item/index.php?page=item">Items</a></li>
                    <?php
                }else{
            ?>
            <?php if($_GET['page']=="user"){?>
                <li class = "nav-link active"><a href="../users/index.php?page=user">Users</a></li>
            <?php }else{?>
                <li class = "nav-link"><a href="../users/index.php?page=user">Users</a></li>    
            <?php }if($_GET['page']=="item"){?>
                <li class = "nav-link active"><a  href="../item/index.php?page=item">Items</a></li>
            <?php }else{?>
                <li class = "nav-link"><a  href="../item/index.php?page=item">Items</a></li>
            <?php }} ?>
            </ul>
            <ul class="nav navbar-nav ml-auto">
                <li class="pull-right"><a href="../login/logout.php">Logout</a></li>
            </ul>
        </div>
        </div>
        </nav>
        <br>
        <!-- last navbar -->
    <?php   
    }
    // lasst sil == 1
// else condition for webpage
}else{
    ?>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
        <a class="navbar-brand" href="../login/login.php">Agria Web</a>
        </div>
    </nav>
    <br>
    <?php
}

if(isset($_SESSION['status'])){
    ?>
    <div class="container">
        <div class="alert alert-success alert-dismissible" role="alert">            
            <strong>Success!</strong> <?php echo $_SESSION['status']?>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>        
        </div>
    </div>
    
    <?php
    unset($_SESSION["status"]);
}else if(isset($_SESSION['danger'])){
    ?>
    <div class="container">
        <div class="alert alert-danger alert-dismissible">    
            <strong>Oops! </strong> <?php echo $_SESSION['danger']?>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>   
        </div>
    </div>
    
    <?php
    unset($_SESSION["danger"]);
}
else if(isset($_SESSION['logout'])){
    ?>
    <div class="container">
        <div class="alert alert-warning alert-dismissible">
            <strong>Success!</strong> <?php echo $_SESSION['logout']?>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>           
        </div>
    </div>
    
    <?php
}

?>

