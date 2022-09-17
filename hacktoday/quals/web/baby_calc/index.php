<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <title>calc</title>
</head>
<style>
.content {
  max-width: 500px;
  margin: auto;
}
</style>
<body>
<div class="content">
<h3>Calculator</h3>
<form action='/' method='post'>
<input type='text' id='input' name='input' />
<input type='submit' class="btn btn-dark"/>
</form>

    
<p><b>
  <?php
 
if (isset($_POST['input'])) {
    $input = $_POST['input'];
    if(!preg_match('/[a-zA-Z`]/', $input) && strlen($input) < 65){
        echo '<br> Result: <br>';
        eval('echo ' . $input . ' ;');
        
    }
    else if (strlen($input) > 65) {
      echo '<br> Result: <br>';
      echo "<p>Too Long</p>";
    }
    else {
      echo '<br> Result: <br>';    
      echo "<p>Not Allowed</p>"; 
    }
}
?>
</b></p> 

</div>
</body>

</html>
