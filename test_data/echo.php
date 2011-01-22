<h1>python-phpserver test page</h1>

<h2>GET</h2>

<?php

foreach ($_GET as $key => $value) {
	echo "<p>$key => $value</p>";
}

?>

<form action="" method="get">
Name: <input type="text" name="name" /><br />
Age: <input type="text" name="age" /><br />
<input type="submit" name="submit" value="Submit" />
</form>

<h2>POST</h2>

<?php

foreach ($_POST as $key => $value) {
	echo "<p>$key => $value</p>";
}

?>

<form action="" method="post">
Name: <input type="text" name="name" /><br />
Age: <input type="text" name="age" /><br />
<input type="submit" name="submit" value="Submit" />
</form>


