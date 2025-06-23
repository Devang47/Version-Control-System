# VCS - Version Control System (C++ Implementation)

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Design](#architecture--design)
3. [Core Components](#core-components)
4. [Technical Implementation](#technical-implementation)
5. [Build & Compilation](#build--compilation)
6. [Usage Examples](#usage-examples)
7. [Security Features](#security-features)
8. [File Structure](#file-structure)

## Project Overview

This is a custom Version Control System (VCS) implemented in C++ that provides basic version control functionality similar to Git. The system manages file versions, handles commits, and provides file encryption for security.

### Key Features
- Repository initialization and management
- File tracking and version control
- Commit history with timestamps
- File reversion to previous versions
- Built-in encryption/decryption for file security
- Cross-platform compatibility (Windows/Linux/macOS)

## Architecture & Design

### Design Principles
1. **Modular Architecture**: Separated into distinct classes for specific responsibilities
2. **Encryption by Default**: All files are encrypted when stored in the repository
3. **Timestamp-based Versioning**: Uses timestamps to uniquely identify file versions
4. **Command-line Interface**: Simple CLI for all operations

### System Architecture
```
VCS System
├── Main Entry Point (main.cpp)
├── Repository Management (repository.h/cpp)
├── Utility Functions (utils.h/cpp)
└── Encryption Module (encryption.h/cpp)
```

## Core Components

### 1. Repository Class (`repository.h/cpp`)

The Repository class is the heart of the VCS system, managing all repository operations.

#### Key Methods:
- `initialize()`: Creates a new repository with directory structure
- `addFile()`: Adds files to the repository with encryption
- `commitFile()`: Creates versioned snapshots of files
- `revertFile()`: Restores files to previous versions
- `checkoutFile()`: Retrieves and decrypts files

#### Repository Structure:
```
MyRepo/
├── config.txt          # Repository configuration
├── commits/             # Directory for versioned files
│   ├── file1.20241201120000    # Committed version with timestamp
│   ├── file1.20241201120000.msg # Optional commit message
│   └── file2.20241201130000
└── file1               # Current encrypted file
```

### 2. Utils Class (`utils.h/cpp`)

Provides essential utility functions for file system operations and cross-platform compatibility.

#### Key Functions:
- `createDirectory()`: Cross-platform directory creation
- `fileExists()` / `directoryExists()`: File system checks
- `getCurrentTimestamp()`: Generates unique timestamps for versioning
- `listFiles()`: Directory traversal with pattern matching
- `copyFileEncrypted()` / `copyFileDecrypted()`: File operations with encryption

### 3. Encryption Class (`encryption.h/cpp`)

Implements XOR-based encryption for file security.

#### Encryption Features:
- XOR cipher with configurable key
- Symmetric encryption (same function for encrypt/decrypt)
- Binary file support
- Default key: "VCS_DEFAULT_KEY_2024"

## Technical Implementation

### 1. Repository Initialization
```cpp
bool Repository::initialize() {
    // Create main repository directory
    if (!Utils::createDirectory(repoPath)) return false;
    
    // Create commits subdirectory for versioned files
    if (!Utils::createDirectory(commitsPath)) return false;
    
    // Create configuration file with metadata
    std::ofstream configFile(configPath);
    configFile << "# VCS Configuration\n";
    configFile << "version=1.0\n";
    configFile << "created=" << Utils::getCurrentTimestamp() << "\n";
    
    return true;
}
```

### 2. File Addition Process
```cpp
bool Repository::addFile(const std::string &filename) {
    // Validate repository state
    if (!isValidRepository()) return false;
    
    // Check if source file exists
    if (!Utils::fileExists(filename)) return false;
    
    // Copy file to repository with encryption
    std::string destPath = repoPath + sep + filename;
    return Utils::copyFileEncrypted(filename, destPath);
}
```

### 3. Commit Mechanism
```cpp
bool Repository::commitFile(const std::string &filename, const std::string &message) {
    // Generate unique timestamp for version identification
    std::string timestamp = Utils::getCurrentTimestamp();
    
    // Create versioned filename: originalname.timestamp
    std::string commitFileName = commitsPath + sep + filename + "." + timestamp;
    
    // Copy current file to commits directory
    if (Utils::copyFile(filePath, commitFileName)) {
        // Save commit message if provided
        if (!message.empty()) {
            std::string messageFile = commitFileName + ".msg";
            // Save message to .msg file
        }
        return true;
    }
    return false;
}
```

### 4. Encryption Implementation
```cpp
std::string Encryption::xorEncrypt(const std::string &data, const std::string &key) {
    std::string result = data;
    size_t keyLen = key.length();
    
    // XOR each byte with corresponding key byte (cycling through key)
    for (size_t i = 0; i < result.length(); ++i) {
        result[i] ^= key[i % keyLen];
    }
    return result;
}
```

### 5. Cross-Platform Compatibility
The system uses C++17 `std::filesystem` for cross-platform file operations:
```cpp
bool Utils::createDirectory(const std::string &path) {
    try {
        if (std::filesystem::exists(path)) return true;
        return std::filesystem::create_directories(path);
    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return false;
    }
}
```

## Build & Compilation

### Makefile Configuration
```makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = myvcs
SOURCES = main.cpp repository.cpp utils.cpp
```

### Build Commands
```bash
# Compile the project
make

# Clean build artifacts
make clean

# Install to system (optional)
make install
```

### Compilation Requirements
- C++17 compatible compiler (GCC 8+, Clang 7+, MSVC 2017+)
- Standard library with filesystem support

## Usage Examples

### 1. Initialize Repository
```bash
./myvcs init MyProject
# Output: Initialized empty VCS repository in MyProject
```

### 2. Add Files
```bash
# Create a sample file
echo "Hello World" > test.txt

# Add to repository (encrypts automatically)
./myvcs add MyProject test.txt
# Output: File added (encrypted): test.txt
```

### 3. Commit Changes
```bash
# Commit with message
./myvcs commit MyProject test.txt "Initial commit"
# Output: File committed (encrypted): test.txt (timestamp: 20241201120000)
```

### 4. View Repository Status
```bash
./myvcs status MyProject
# Output:
# Repository: MyProject
# Tracked files (1):
#   test.txt
# Total commits: 1
```

### 5. Revert to Previous Version
```bash
# Revert to specific timestamp
./myvcs revert MyProject test.txt 20241201120000
# Output: File reverted (decrypted) to: test.txt.20241201120000
```

## Security Features

### 1. Encryption Strategy
- **Algorithm**: XOR cipher with configurable key
- **Key Management**: Default key embedded, can be customized
- **File Protection**: All repository files encrypted at rest

### 2. Security Benefits
- Prevents casual inspection of versioned files
- Protects against accidental exposure
- Maintains file integrity through versioning

### 3. Security Limitations
- XOR encryption is not cryptographically secure
- Key is embedded in source code
- Suitable for basic protection, not sensitive data

## File Structure

### Source Code Organization
```
Version Control System/
├── main.cpp              # CLI interface and command handling
├── repository.h/cpp      # Core repository management
├── utils.h/cpp          # Utility functions and file operations
├── encryption.h/cpp     # File encryption/decryption
├── Makefile            # Build configuration
└── myvcs               # Compiled executable
```

### Repository Structure (Example)
```
MyProject/
├── config.txt                    # Repository metadata
├── commits/                      # Version history
│   ├── README.md.20241201120000  # First commit
│   ├── README.md.20241201120000.msg # Commit message
│   ├── README.md.20241201130000  # Second commit
│   └── main.cpp.20241201140000   # Another file's commit
├── README.md                     # Current encrypted file
└── main.cpp                     # Current encrypted file
```

## Technical Highlights for Examination

### 1. Object-Oriented Design
- **Encapsulation**: Private members in Repository class
- **Separation of Concerns**: Each class has specific responsibility
- **Modularity**: Independent components that can be tested separately

### 2. Memory Management
- RAII principles with automatic resource cleanup
- No manual memory allocation (uses standard containers)
- Exception-safe operations with proper error handling

### 3. Error Handling
- Comprehensive error checking for file operations
- Graceful failure with informative error messages
- Input validation at multiple levels

### 4. Performance Considerations
- Efficient file copying with binary streams
- Minimal memory footprint for file operations
- Timestamp-based indexing for quick version lookup

### 5. Extensibility
- Pluggable encryption system
- Configurable repository structure
- Easy to add new commands through main.cpp dispatch

## Implementation Challenges Solved

1. **Cross-Platform Compatibility**: Used C++17 filesystem library
2. **File Encryption**: Implemented efficient XOR cipher
3. **Version Management**: Timestamp-based unique identification
4. **Error Handling**: Comprehensive validation and error reporting
5. **CLI Design**: Intuitive command structure similar to Git

This VCS demonstrates practical application of C++ features including file I/O, object-oriented design, standard library usage, and cross-platform development techniques.
