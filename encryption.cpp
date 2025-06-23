#include "encryption.h"
#include <fstream>
#include <iostream>

namespace VCS
{
  bool Encryption::encryptFile(const std::string &inputFile, const std::string &outputFile, const std::string &key)
  {
    std::ifstream input(inputFile, std::ios::binary);
    if (!input)
    {
      std::cerr << "Failed to open input file for encryption: " << inputFile << std::endl;
      return false;
    }

    std::string content((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
    input.close();

    std::string encrypted = xorEncrypt(content, key);

    std::ofstream output(outputFile, std::ios::binary);
    if (!output)
    {
      std::cerr << "Failed to create encrypted output file: " << outputFile << std::endl;
      return false;
    }

    output.write(encrypted.c_str(), encrypted.size());
    output.close();

    return true;
  }

  bool Encryption::decryptFile(const std::string &inputFile, const std::string &outputFile, const std::string &key)
  {
    std::ifstream input(inputFile, std::ios::binary);
    if (!input)
    {
      std::cerr << "Failed to open encrypted file: " << inputFile << std::endl;
      return false;
    }

    std::string content((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
    input.close();

    std::string decrypted = xorDecrypt(content, key);

    std::ofstream output(outputFile, std::ios::binary);
    if (!output)
    {
      std::cerr << "Failed to create decrypted output file: " << outputFile << std::endl;
      return false;
    }

    output.write(decrypted.c_str(), decrypted.size());
    output.close();

    return true;
  }

  std::string Encryption::xorEncrypt(const std::string &data, const std::string &key)
  {
    std::string result = data;
    size_t keyLen = key.length();

    for (size_t i = 0; i < result.length(); ++i)
    {
      result[i] ^= key[i % keyLen];
    }

    return result;
  }

  std::string Encryption::xorDecrypt(const std::string &data, const std::string &key)
  {
    // XOR encryption is symmetric, so decryption is the same as encryption
    return xorEncrypt(data, key);
  }
}
