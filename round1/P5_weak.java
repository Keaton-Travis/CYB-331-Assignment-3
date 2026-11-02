import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public void saveUploadedFile(MultipartFile file, String uploadDirectory) throws IOException {
    if (file.isEmpty()) {
        throw new IllegalArgumentException("Failed to store empty file.");
    }

    // Resolve the upload directory path
    Path uploadPath = Paths.get(uploadDirectory);

    // Create the directory if it does not exist
    if (!Files.exists(uploadPath)) {
        Files.createDirectories(uploadPath);
    }

    // Resolve the destination file path using the original filename
    Path filePath = uploadPath.resolve(file.getOriginalFilename());

    // Copy the file contents to the destination path
    Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
}