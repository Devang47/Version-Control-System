#ifndef REPOSITORY_H
#define REPOSITORY_H

#include <string>
#include <vector>

namespace VCS
{
  struct CommitInfo
  {
    std::string filename;
    std::string timestamp;
    std::string fullPath;
  };

  class Repository
  {
  private:
    std::string repoPath;
    std::string commitsPath;
    std::string configPath;

  public:
    Repository(const std::string &path);

    bool initialize();
    bool isValidRepository() const;
    bool addFile(const std::string &filename);
    bool commitFile(const std::string &filename, const std::string &message = "");
    bool revertFile(const std::string &filename, const std::string &timestamp = "");
    bool checkoutFile(const std::string &filename);

    std::vector<std::string> getTrackedFiles() const;
    std::vector<CommitInfo> getCommitHistory(const std::string &filename = "") const;
    std::string getStatus() const;

    const std::string &getRepoPath() const { return repoPath; }
    const std::string &getCommitsPath() const { return commitsPath; }
  };
}

#endif
