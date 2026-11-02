<?php
// Initialize variables
$user_comment = '';
$submitted = false;

// Check if the form was submitted via POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['comment'])) {
        // Trim whitespace and escape special HTML characters to prevent XSS
        $user_comment = htmlspecialchars(trim($_POST['comment']), ENT_QUOTES, 'UTF-8');
        $submitted = true;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comment Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .form-container { max-width: 500px; margin-bottom: 20px; }
        textarea { width: 100%; height: 100px; padding: 10px; margin-bottom: 10px; }
        button { padding: 10px 15px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .output { background-color: #f4f4f4; padding: 15px; border-left: 4px solid #007BFF; max-width: 500px; }
    </style>
</head>
<body>

    <h2>Leave a Comment</h2>

    <div class="form-container">
        <form method="POST" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">
            <label for="comment">Your Comment:</label><br>
            <textarea id="comment" name="comment" required></textarea><br>
            <button type="submit">Submit Comment</button>
        </form>
    </div>

    <?php if ($submitted): ?>
        <div class="output">
            <h3>Your Submitted Comment:</h3>
            <p><?php echo nl2br($user_comment); ?></p>
        </div>
    <?php endif; ?>

</body>
</html>