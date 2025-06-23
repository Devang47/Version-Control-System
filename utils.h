#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>

namespace VCS
{
  class Utils
  {
  public:
    static bool createDirectory(const std::string &path);
    static bool directoryExists(const std::string &path);
    static bool fileExists(const std::string &path);
    static std::string getCurrentTimestamp();
    static std::vector<std::string> listFiles(const std::string &directory, const std::string &pattern = "");
    static bool copyFile(const std::string &source, const std::string &destination);
    static bool copyFileEncrypted(const std::string &source, const std::string &destination);
    static bool copyFileDecrypted(const std::string &source, const std::string &destination);
    static std::string getPathSeparator();
  };
}

#endif
