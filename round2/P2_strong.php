<?php
$error = null;
$sanitized_comment = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['comment'])) {
        $raw_comment = $_POST['comment'];

        // 1. Reject null bytes to prevent injection bypasses
        if (str_contains($raw_comment, "\0")) {
            $error = "An error occurred while processing your comment.";
        } 
        // 2. Validate character length (max 1,000 characters using UTF-8-safe mb_strlen)
        elseif (mb_strlen($raw_comment, 'UTF-8') > 1000) {
            $error = "An error occurred while processing your comment.";
        } else {
            // 3. Defend against XSS by using htmlspecialchars with ENT_QUOTES, ENT_SUBSTITUTE, and UTF-8 charset
            $sanitized_comment = htmlspecialchars($raw_comment, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
        }
    } else {
        $error = "An error occurred while processing your comment.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comment Form</title>
</head>
<body>

    <h1>Leave a Comment</h1>

    <?php if ($error !== null): ?>
        <p style="color: red;"><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></p>
    <?php elseif ($_SERVER['REQUEST_METHOD'] === 'POST' && $error === null): ?>
        <div>
            <h3>Your Submitted Comment:</h3>
            <p><?php echo $sanitized_comment; ?></p>
        </div>
        <hr>
    <?php endif; ?>

    <form method="POST" action="">
        <label for="comment">Comment (maximum 1,000 characters):</label><br>
        <textarea id="comment" name="comment" rows="5" cols="50" maxlength="1000" required></textarea><br><br>
        <button type="submit">Submit Comment</button>
    </form>

</body>
</html>