import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Objects;

public class FileUploadService {

    private final Path rootLocation = Paths.get("uploads");

    public String saveFile(MultipartFile file) throws IOException {
        // Ensure the directory exists
        if (!Files.exists(rootLocation)) {
            Files.createDirectories(rootLocation);
        }

        if (file.isEmpty()) {
            throw new IllegalArgumentException("Cannot save an empty file.");
        }

        // Clean and sanitize the original filename
        String originalFilename = Objects.requireNonNull(file.getOriginalFilename());
        String cleanFilename = Paths.get(originalFilename).getFileName().toString();

        // Prevent Directory Traversal Attack
        Path destinationFile = rootLocation.resolve(cleanFilename).normalize().toAbsolutePath();
        if (!destinationFile.getParent().equals(rootLocation.toAbsolutePath())) {
            throw new SecurityException("Cannot store file outside current directory.");
        }

        // Save file input stream to destination path (overwriting if file exists)
        try (InputStream inputStream = file.getInputStream()) {
            Files.copy(inputStream, destinationFile, StandardCopyOption.REPLACE_EXISTING);
        }

        return destinationFile.toString();
    }
}