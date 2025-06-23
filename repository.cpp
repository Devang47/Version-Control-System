#include "repository.h"
#include "utils.h"
#include <iostream>
#include <fstream>
#include <sstream>

namespace VCS
{
  Repository::Repository(const std::string &path)
      : repoPath(path)
  {
    std::string sep = Utils::getPathSeparator();
    commitsPath = repoPath + sep + "commits";
    configPath = repoPath + sep + "config.txt";
  }

  bool Repository::initialize()
  {
    if (!Utils::createDirectory(repoPath))
    {
      return false;
    }

    if (!Utils::createDirectory(commitsPath))
    {
      return false;
    }

    // Create config file
    std::ofstream configFile(configPath);
    if (configFile)
    {
      configFile << "# VCS Configuration\n";
      configFile << "version=1.0\n";
      configFile << "created=" << Utils::getCurrentTimestamp() << "\n";
      configFile.close();
    }

    std::cout << "Initialized empty VCS repository in " << repoPath << std::endl;
    return true;
  }

  bool Repository::isValidRepository() const
  {
    return Utils::directoryExists(repoPath) &&
           Utils::directoryExists(commitsPath) &&
           Utils::fileExists(configPath);
  }

  bool Repository::addFile(const std::string &filename)
  {
    if (!isValidRepository())
    {
      std::cerr << "Not a valid VCS repository" << std::endl;
      return false;
    }

    if (!Utils::fileExists(filename))
    {
      std::cerr << "File not found: " << filename << std::endl;
      return false;
    }

    std::string sep = Utils::getPathSeparator();
    std::string destPath = repoPath + sep + filename;

    if (Utils::copyFileEncrypted(filename, destPath))
    {
      std::cout << "File added (encrypted): " << filename << std::endl;
      return true;
    }

    std::cerr << "Failed to add file: " << filename << std::endl;
    return false;
  }

  bool Repository::commitFile(const std::string &filename, const std::string &message)
  {
    if (!isValidRepository())
    {
      std::cerr << "Not a valid VCS repository" << std::endl;
      return false;
    }

    std::string sep = Utils::getPathSeparator();
    std::string filePath = repoPath + sep + filename;

    if (!Utils::fileExists(filePath))
    {
      std::cerr << "File not found in repository: " << filename << std::endl;
      return false;
    }

    std::string timestamp = Utils::getCurrentTimestamp();
    std::string commitFileName = commitsPath + sep + filename + "." + timestamp;

    if (Utils::copyFile(filePath, commitFileName))
    {
      // Save commit message if provided
      if (!message.empty())
      {
        std::string messageFile = commitFileName + ".msg";
        std::ofstream msgFile(messageFile);
        if (msgFile)
        {
          msgFile << message << std::endl;
          msgFile.close();
        }
      }

      std::cout << "File committed (encrypted): " << filename << " (timestamp: " << timestamp << ")" << std::endl;
      return true;
    }

    std::cerr << "Failed to commit file: " << filename << std::endl;
    return false;
  }

  bool Repository::revertFile(const std::string &filename, const std::string &timestamp)
  {
    if (!isValidRepository())
    {
      std::cerr << "Not a valid VCS repository" << std::endl;
      return false;
    }

    std::vector<std::string> commits = Utils::listFiles(commitsPath, filename + ".");
    if (commits.empty())
    {
      std::cerr << "No commits found for file: " << filename << std::endl;
      return false;
    }

    std::string targetCommit;
    if (!timestamp.empty())
    {
      std::string targetFile = filename + "." + timestamp;
      for (const auto &commit : commits)
      {
        if (commit == targetFile)
        {
          targetCommit = commit;
          break;
        }
      }
      if (targetCommit.empty())
      {
        std::cerr << "No commit found with timestamp: " << timestamp << std::endl;
        return false;
      }
    }
    else
    {
      // Use the latest commit
      targetCommit = commits.back();
    }

    std::string sep = Utils::getPathSeparator();
    std::string commitFilePath = commitsPath + sep + targetCommit;
    std::string filePath = repoPath + sep + filename;

    if (Utils::copyFileDecrypted(commitFilePath, filePath))
    {
      std::cout << "File reverted (decrypted) to: " << targetCommit << std::endl;
      return true;
    }

    std::cerr << "Failed to revert file: " << filename << std::endl;
    return false;
  }

  bool Repository::checkoutFile(const std::string &filename)
  {
    if (!isValidRepository())
    {
      std::cerr << "Not a valid VCS repository" << std::endl;
      return false;
    }

    std::string sep = Utils::getPathSeparator();
    std::string encryptedFilePath = repoPath + sep + filename;

    if (!Utils::fileExists(encryptedFilePath))
    {
      std::cerr << "File not found in repository: " << filename << std::endl;
      return false;
    }

    // Create output filename with .decrypted extension to avoid overwriting
    std::string outputFilename = filename + ".decrypted";

    if (Utils::copyFileDecrypted(encryptedFilePath, outputFilename))
    {
      std::cout << "File checked out (decrypted) as: " << outputFilename << std::endl;
      return true;
    }

    std::cerr << "Failed to checkout file: " << filename << std::endl;
    return false;
  }

  std::vector<std::string> Repository::getTrackedFiles() const
  {
    if (!isValidRepository())
    {
      return {};
    }

    return Utils::listFiles(repoPath);
  }

  std::vector<CommitInfo> Repository::getCommitHistory(const std::string &filename) const
  {
    std::vector<CommitInfo> history;
    if (!isValidRepository())
    {
      return history;
    }

    std::string pattern = filename.empty() ? "" : filename + ".";
    std::vector<std::string> commits = Utils::listFiles(commitsPath, pattern);

    for (const auto &commit : commits)
    {
      if (commit.find(".msg") != std::string::npos)
        continue; // Skip message files

      CommitInfo info;
      size_t dotPos = commit.find_last_of('.');
      if (dotPos != std::string::npos)
      {
        info.filename = commit.substr(0, dotPos);
        info.timestamp = commit.substr(dotPos + 1);
        info.fullPath = commitsPath + Utils::getPathSeparator() + commit;
        history.push_back(info);
      }
    }

    return history;
  }

  std::string Repository::getStatus() const
  {
    if (!isValidRepository())
    {
      return "Not a valid VCS repository";
    }

    std::stringstream status;
    status << "Repository: " << repoPath << "\n";

    std::vector<std::string> files = getTrackedFiles();
    status << "Tracked files (" << files.size() << "):\n";
    for (const auto &file : files)
    {
      status << "  " << file << "\n";
    }

    std::vector<CommitInfo> history = getCommitHistory();
    status << "Total commits: " << history.size() << "\n";

    return status.str();
  }
}
