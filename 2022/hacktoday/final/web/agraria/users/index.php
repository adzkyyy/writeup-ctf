<?php
include "../header.php";
include "../isAuthenticated.php";
?>
</head>
<body>
    <div class="container">
    <h1>List User</h1>
    <table class="table table-hover">
        <thead>
            <tr>
                <style>
                    th,td{
                        text-align: center;
                    }
                </style>
                <th>NO</th>
                <th>username</th>
                <th>Gender</th>
                <th>Id Level</th>
            </tr>
        </thead>
        <tbody>
            <?php
                $data = mysqli_query($conn, "SELECT * FROM user ORDER BY id ASC");
                while($result= mysqli_fetch_array($data)){
                    ?>
			<tr>
				<td><?php echo $result['id']; ?></td>
				<td><?php echo htmlentities($result['username']); ?></td>
                <td><?php echo htmlentities($result['gender']); ?></td>
                <td><?php echo $result['id_level']; ?></td>
			</tr>
			<?php 
                }
            ?>
        </tbody>
    </table>
    </div>
</body>
</html>