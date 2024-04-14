<?php
// Establish SQLite database connection
$db = new SQLite3('data.db');

// Query to fetch name and price of menu items from the database
$query = "SELECT name, price FROM menu";
$result = $db->query($query);

// Output HTML for menu items
while ($row = $result->fetchArray()) {
    echo '<li class="nav-item"><a class="nav-link" href="#">' . $row['name'] . ' - $' . $row['price'] . '</a></li>';
}

// Close the database connection
$db->close();
?>
