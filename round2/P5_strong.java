import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class P5_strong {

    private static final Logger logger = LoggerFactory.getLogger(P5_strong.class);
    
    // 2 MB in bytes
    private static final long MAX_FILE_SIZE = 2 * 1024 * 1024; 
    
    // Configured safe upload directory (absolute and normalized)
    private final Path uploadDir = Paths.get("uploads").toAbsolutePath().normalize();

    // Known dangerous executable magic bytes / signatures to block (e.g., Windows PE / ELF)
    private static final List<byte[]> FORBIDDEN_SIGNATURES = Arrays.asList(
        new byte[] { (byte) 0x4D, (byte) 0x5A }, // Windows PE / EXE / DLL ("MZ")
        new byte[] { 0x7F, 0x45, 0x4C, 0x46 }       // Linux ELF executable
    );

    /**
     * Saves an uploaded file securely with validation, path traversal defense, 
     * magic byte inspection, and cryptographic UUID naming.
     *
     * @param file             The uploaded multipart file
     * @param expectedExtension The expected file extension (e.g., ".png" or "jpg")
     * @return The securely generated unique filename
     */
    public String saveUploadedFile(MultipartFile file, String expectedExtension) throws IOException, SecurityException {
        
        // 1. Validate File Size (Max 2 MB)
        if (file == null || file.isEmpty()) {
            logger.warn("File upload failed: Uploaded file is null or empty.");
            throw new IllegalArgumentException("The uploaded file cannot be empty.");
        }
        
        if (file.getSize() > MAX_FILE_SIZE) {
            logger.warn("File upload failed: File size {} bytes exceeds the 2 MB limit.", file.getSize());
            throw new IllegalArgumentException("File size exceeds the maximum allowed limit of 2 MB.");
        }

        // 2. Validate and Sanitize the Expected Extension
        String sanitizedExtension = sanitizeExtension(expectedExtension);

        // 3. Inspect Magic Bytes (Header bytes) to prevent executable uploads
        try (InputStream is = file.getInputStream()) {
            byte[] headerBytes = new byte[8];
            int bytesRead = is.read(headerBytes);
            if (bytesRead > 0) {
                for (byte[] forbiddenSig : FORBIDDEN_SIGNATURES) {
                    if (startsWith(headerBytes, forbiddenSig)) {
                        logger.warn("Security warning: Uploaded file contains forbidden executable magic bytes.");
                        throw new SecurityException("Security violation: Uploaded file contains disallowed executable headers.");
                    }
                }
            }
        } catch (IOException e) {
            logger.warn("File upload failed while reading file stream for magic bytes check: {}", e.getMessage());
            throw new IOException("Failed to read uploaded file stream.", e);
        }

        // 4. Generate Cryptographically Secure UUID Filename (ignoring original filename)
        String uniqueFilename = UUID.randomUUID().toString() + sanitizedExtension;

        // 5. Ensure Upload Directory Exists
        if (!Files.exists(uploadDir)) {
            Files.createDirectories(uploadDir);
        }

        // 6. Defend Against Path Traversal by resolving and validating target path
        Path targetPath = uploadDir.resolve(uniqueFilename).normalize();
        if (!targetPath.startsWith(uploadDir)) {
            logger.warn("Path traversal attempt detected and blocked: {}", targetPath);
            throw new SecurityException("Invalid file path resolution.");
        }

        // 7. Save File to Disk
        try (InputStream inputStream = file.getInputStream()) {
            Files.copy(inputStream, targetPath, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            logger.warn("Failed to store file on disk: {}", e.getMessage());
            throw new IOException("Failed to store file securely on the server.", e);
        }

        logger.info("File successfully uploaded and saved as: {}", uniqueFilename);
        return uniqueFilename;
    }

    /**
     * Sanitizes and validates the expected extension format.
     */
    private String sanitizeExtension(String ext) {
        if (ext == null || ext.isBlank()) {
            logger.warn("File upload failed: Expected extension is missing or blank.");
            throw new IllegalArgumentException("Expected file extension is required.");
        }
        String clean = ext.trim().toLowerCase();
        if (!clean.startsWith(".")) {
            clean = "." + clean;
        }
        // Allow only alphanumeric extensions between 1 and 10 characters long
        if