#include "utils.h"
#include "encryption.h"
#include <iostream>
#include <fstream>
#include <ctime>
#include <filesystem>
#include <algorithm>

#ifdef _WIN32
#include <windows.h>
#include <direct.h>
#else
#include <sys/stat.h>
#include <dirent.h>
#endif

namespace VCS
{
  bool Utils::createDirectory(const std::string &path)
  {
    try
    {
      if (std::filesystem::exists(path))
      {
        std::cout << "Directory already exists: " << path << std::endl;
        return true;
      }

      if (std::filesystem::create_directories(path))
      {
        std::cout << "Created: " << path << std::endl;
        return true;
      }
    }
    catch (const std::exception &e)
    {
      std::cerr << "Failed to create directory " << path << ": " << e.what() << std::endl;
    }
    return false;
  }

  bool Utils::directoryExists(const std::string &path)
  {
    return std::filesystem::exists(path) && std::filesystem::is_directory(path);
  }

  bool Utils::fileExists(const std::string &path)
  {
    return std::filesystem::exists(path) && std::filesystem::is_regular_file(path);
  }

  std::string Utils::getCurrentTimestamp()
  {
    time_t now = time(0);
    char timestamp[20];
    strftime(timestamp, sizeof(timestamp), "%Y%m%d%H%M%S", localtime(&now));
    return std::string(timestamp);
  }

  std::vector<std::string> Utils::listFiles(const std::string &directory, const std::string &pattern)
  {
    std::vector<std::string> files;
    try
    {
      for (const auto &entry : std::filesystem::directory_iterator(directory))
      {
        if (entry.is_regular_file())
        {
          std::string filename = entry.path().filename().string();
          if (pattern.empty() || filename.find(pattern) != std::string::npos)
          {
            files.push_back(filename);
          }
        }
      }
      std::sort(files.begin(), files.end());
    }
    catch (const std::exception &e)
    {
      std::cerr << "Error listing files: " << e.what() << std::endl;
    }
    return files;
  }

  bool Utils::copyFile(const std::string &source, const std::string &destination)
  {
    try
    {
      std::filesystem::copy_file(source, destination, std::filesystem::copy_options::overwrite_existing);
      return true;
    }
    catch (const std::exception &e)
    {
      std::cerr << "Error copying file: " << e.what() << std::endl;
      return false;
    }
  }

  bool Utils::copyFileEncrypted(const std::string &source, const std::string &destination)
  {
    return Encryption::encryptFile(source, destination);
  }

  bool Utils::copyFileDecrypted(const std::string &source, const std::string &destination)
  {
    return Encryption::decryptFile(source, destination);
  }

  std::string Utils::getPathSeparator()
  {
    return std::string(1, std::filesystem::path::preferred_separator);
  }
}
