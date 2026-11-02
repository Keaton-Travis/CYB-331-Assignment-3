<?php
$comment = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Deliberately insecure: storing and displaying raw user input without escaping
    $comment = $_POST['comment'] ?? '';
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Insecure Comment Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .comment-box { border: 1px solid #ccc; padding: 15px; margin-top: 20px; background: #f9f9f9; }
    </style>
</head>
<body>

    <h2>Leave a Comment</h2>
    <form method="POST" action="">
        <label for="comment">Your Comment:</label><br><br>
        <textarea name="comment" id="comment" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Submit Comment">
    </form>

    <?php if (!empty($comment)): ?>
        <div class="comment-box">
            <h3>Submitted Comment:</h3>
            <!-- Vulnerability: raw echo allows execution of arbitrary HTML/JavaScript -->
            <p><?php echo $comment; ?></p>
        </div>
    <?php endif; ?>

</body>
</html>