#ifndef ENCRYPTION_H
#define ENCRYPTION_H

#include <string>

namespace VCS
{
  class Encryption
  {
  public:
    static bool encryptFile(const std::string &inputFile, const std::string &outputFile, const std::string &key = "VCS_DEFAULT_KEY_2024");
    static bool decryptFile(const std::string &inputFile, const std::string &outputFile, const std::string &key = "VCS_DEFAULT_KEY_2024");

  private:
    static std::string xorEncrypt(const std::string &data, const std::string &key);
    static std::string xorDecrypt(const std::string &data, const std::string &key);
  };
}

#endif
