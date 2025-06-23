#include <iostream>
#include <string>
#include <vector>
#include "repository.h"

using namespace std;
using namespace VCS;

void printUsage()
{
  cout << "VCS - Simple Version Control System\n";
  cout << "Usage:\n";
  cout << "  myvcs init <repo>                    - Initialize a new repository\n";
  cout << "  myvcs add <repo> <filename>          - Add a file to the repository\n";
  cout << "  myvcs commit <repo> <filename> [msg] - Commit a file with optional message\n";
  cout << "  myvcs revert <repo> <filename> [timestamp] - Revert file to specific version\n";
  cout << "  myvcs checkout <repo> <filename>     - Retrieve and decrypt file from repository\n";
  cout << "  myvcs status <repo>                  - Show repository status\n";
  cout << "  myvcs log <repo> [filename]          - Show commit history\n";
}

void handleInit(const vector<string> &args)
{
  if (args.size() < 3)
  {
    cerr << "Usage: myvcs init <repo>\n";
    return;
  }

  Repository repo(args[2]);
  if (repo.initialize())
  {
    cout << "Repository initialized successfully.\n";
  }
}

void handleAdd(const vector<string> &args)
{
  if (args.size() < 4)
  {
    cerr << "Usage: myvcs add <repo> <filename>\n";
    return;
  }

  Repository repo(args[2]);
  if (repo.addFile(args[3]))
  {
    cout << "File " << args[3] << " added to repository.\n";
  }
}

void handleCommit(const vector<string> &args)
{
  if (args.size() < 4)
  {
    cerr << "Usage: myvcs commit <repo> <filename> [message]\n";
    return;
  }

  string message = (args.size() >= 5) ? args[4] : "";
  Repository repo(args[2]);
  if (repo.commitFile(args[3], message))
  {
    cout << "File " << args[3] << " committed.\n";
  }
}

void handleRevert(const vector<string> &args)
{
  if (args.size() < 4)
  {
    cerr << "Usage: myvcs revert <repo> <filename> [timestamp]\n";
    return;
  }

  string timestamp = (args.size() >= 5) ? args[4] : "";
  Repository repo(args[2]);
  if (repo.revertFile(args[3], timestamp))
  {
    cout << "File " << args[3] << " reverted.\n";
  }
}

void handleCheckout(const vector<string> &args)
{
  if (args.size() < 4)
  {
    cerr << "Usage: myvcs checkout <repo> <filename>\n";
    return;
  }

  Repository repo(args[2]);
  if (repo.checkoutFile(args[3]))
  {
    cout << "File " << args[3] << " checked out and decrypted.\n";
  }
}

void handleStatus(const vector<string> &args)
{
  if (args.size() < 3)
  {
    cerr << "Usage: myvcs status <repo>\n";
    return;
  }

  Repository repo(args[2]);
  cout << repo.getStatus();
}

void handleLog(const vector<string> &args)
{
  if (args.size() < 3)
  {
    cerr << "Usage: myvcs log <repo> [filename]\n";
    return;
  }

  string filename = (args.size() >= 4) ? args[3] : "";
  Repository repo(args[2]);

  vector<CommitInfo> history = repo.getCommitHistory(filename);
  if (history.empty())
  {
    cout << "No commits found.\n";
    return;
  }

  cout << "Commit History:\n";
  for (const auto &commit : history)
  {
    cout << "File: " << commit.filename << " | Timestamp: " << commit.timestamp << "\n";
  }
}

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    printUsage();
    return 1;
  }

  vector<string> args;
  for (int i = 0; i < argc; i++)
  {
    args.push_back(string(argv[i]));
  }

  string command = args[1];

  if (command == "init")
  {
    handleInit(args);
  }
  else if (command == "add")
  {
    handleAdd(args);
  }
  else if (command == "commit")
  {
    handleCommit(args);
  }
  else if (command == "revert")
  {
    handleRevert(args);
  }
  else if (command == "checkout")
  {
    handleCheckout(args);
  }
  else if (command == "status")
  {
    handleStatus(args);
  }
  else if (command == "log")
  {
    handleLog(args);
  }
  else
  {
    cerr << "Unknown command: " << command << "\n";
    printUsage();
    return 1;
  }

  return 0;
}
