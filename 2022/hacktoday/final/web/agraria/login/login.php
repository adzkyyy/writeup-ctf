<?php
include "../header.php";
?>
</head>
<body>

    <div class="container d-flex justify-content-center align-items-center"
      style="min-height: 75vh">
      	<form class="border shadow p-3 rounded" action="checkLogin.php" method="post" style="width: 450px;">      
            <h1 class="text-center p-3">LOGIN</h1>
		  <div class="mb-3">
		    <label for="username" 
		           class="form-label">Username : </label>
		    <input type="text" 
		           class="form-control" 
		           name="username" 
		           id="username">
		  </div>
		  <div class="mb-3">
		    <label for="password" 
		           class="form-label">Password : </label>
		    <input type="password" 
		           name="password" 
		           class="form-control" 
		           id="password">
		  </div>
		 
		  <button type="submit" 
		          class="btn btn-primary">LOGIN</button>
            <a href="pageReset.php">Forgot Your Password?</a>
		</form>
      </div>

</body>
</html>
