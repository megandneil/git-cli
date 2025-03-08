#!/usr/bin/env python3
import os
import sys
import yaml
from dulwich import porcelain
from dulwich.repo import Repo

# Utility to load a YAML file
def load_yaml_file(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

# Interactive command loop
def interactive_loop(repo_config):
    local_path = repo_config.get("local_path", "my_repo")
    repo_url = repo_config.get("url", "")
    default_commit_message = repo_config.get("default_commit_message", "Default commit message")

    # Check if a repository already exists locally (i.e. a .git folder exists)
    repo = None
    if os.path.exists(os.path.join(local_path, ".git")):
        try:
            repo = Repo(local_path)
            print(f"Opened existing repository at '{local_path}'.")
        except Exception as e:
            print("Error opening repository:", e)
    else:
        print("No local repository found. You can 'clone' or 'init' one.")

    print("\nWelcome to the interactive Git CLI!")
    print("Type 'help' to see available commands.\n")

    while True:
        command = input("git-cli> ").strip()
        if command in ["exit", "quit"]:
            print("Exiting CLI.")
            break
        elif command == "help":
            print("\nAvailable commands:")
            print("  clone                - Clone the repository from remote")
            print("  init                 - Initialize a new local repository")
            print("  status               - Show repository status")
            print("  stage <file(s)>      - Stage file(s) (separated by space)")
            print("  commit               - Commit staged changes (with a prompt for message)")
            print("  log                  - Show commit log")
            print("  push                 - Push changes to remote")
            print("  help                 - Show this help message")
            print("  exit/quit            - Exit the CLI\n")
        elif command.startswith("clone"):
            if repo is None:
                print(f"Cloning repository from {repo_url} into '{local_path}'...")
                try:
                    porcelain.clone(repo_url, local_path)
                    repo = Repo(local_path)
                    print("Repository cloned successfully.")
                except Exception as e:
                    print("Error cloning repository:", e)
            else:
                print("Local repository already exists.")
        elif command.startswith("init"):
            if repo is None:
                print(f"Initializing new repository at '{local_path}'...")
                try:
                    porcelain.init(local_path)
                    repo = Repo(local_path)
                    print("Repository initialized.")
                except Exception as e:
                    print("Error initializing repository:", e)
            else:
                print("Local repository already exists.")
        elif command.startswith("status"):
            if repo is None:
                print("Repository not found. Please 'clone' or 'init' first.")
            else:
                try:
                    # Dulwich doesn't have a status command exactly like Git.
                    # Here we simulate a basic status: list untracked files.
                    
                    
                    
                    
                    ############
                    '''
                    '''
                    
                    # nw: tracked = set(repo.get_index().iterkeys())
                    
                    index = repo.open_index()
                    # nw: tracked = set(index.iterkeys())
                    # nw: tracked = set(index.keys())
                    # nw: tracked = set(index.entries.keys())
                    # tracked = set(repo.open_index().iterblobs())
                    #index = repo.open_index()
                    #print(dir(index))
                    #tracked = {entry.path.decode('utf-8') if isinstance(entry.path, bytes) else entry.path for entry in index}
                    tracked = {path.decode('utf-8') if isinstance(path, bytes) else path for path in index.paths()}
                    '''
                    '''
                    ###########
                    all_files = set()
                    for root, _, files in os.walk(local_path):
                        for file in files:
                            filepath = os.path.relpath(os.path.join(root, file), local_path)
                            if filepath != ".git/HEAD" and ".git" not in filepath:
                                all_files.add(filepath)
                    untracked = all_files - set(f.decode('utf-8') if isinstance(f, bytes) else f for f in tracked)
                    print("\nTracked files:")
                    for f in tracked:
                        print("  ", f.decode('utf-8') if isinstance(f, bytes) else f)
                    print("\nUntracked files:")
                    for f in untracked:
                        print("  ", f)
                    print("")
                except Exception as e:
                    print("Error getting status:", e)
        elif command.startswith("stage"):
            if repo is None:
                print("Repository not found. Please 'clone' or 'init' first.")
            else:
                parts = command.split()
                if len(parts) < 2:
                    print("Usage: stage <file1> [file2 ...]")
                else:
                    files_to_stage = parts[1:]
                    try:
                        porcelain.add(local_path, paths=files_to_stage)
                        print("Staged files:", files_to_stage)
                    except Exception as e:
                        print("Error staging files:", e)
        elif command.startswith("commit"):
            if repo is None:
                print("Repository not found. Please 'clone' or 'init' first.")
            else:
                message = input(f"Enter commit message (default: '{default_commit_message}'): ").strip()
                if not message:
                    message = default_commit_message
                confirm = input(f"Commit with message: '{message}'? (y/n): ").strip().lower()
                if confirm == "y":
                    try:
                        porcelain.commit(local_path, message=message.encode('utf-8'))
                        print("Commit successful.")
                    except Exception as e:
                        print("Error committing changes:", e)
                else:
                    print("Commit cancelled.")
        elif command.startswith("log"):
            if repo is None:
                print("Repository not found. Please 'clone' or 'init' first.")
            else:
                try:
                    print("\nCommit Log:")
                    walker = repo.get_walker()
                    for entry in walker:
                        commit = entry.commit
                        commit_id = commit.id.decode('utf-8') if isinstance(commit.id, bytes) else commit.id
                        author = commit.author.decode('utf-8') if isinstance(commit.author, bytes) else commit.author
                        timestamp = commit.commit_time
                        # Convert commit_time to a human-readable format if desired
                        print(f"Commit: {commit_id}")
                        print(f"Author: {author}")
                        print(f"Date: {timestamp}")
                        msg = commit.message.decode('utf-8').strip() if isinstance(commit.message, bytes) else commit.message.strip()
                        print(f"Message: {msg}")
                        print("-" * 40)
                    print("")
                except Exception as e:
                    print("Error displaying log:", e)
        elif command.startswith("push"):
            if repo is None:
                print("Repository not found. Please 'clone' or 'init' first.")
            else:
                try:
                    print("Pushing changes to remote...")
                    porcelain.push(local_path, repo_url)
                    print("Push successful.")
                except Exception as e:
                    print("Error pushing changes:", e)
        else:
            print("Unknown command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    # Load configuration from config.yaml
    try:
        config = load_yaml_file("config.yaml")
    except Exception as e:
        print("Error loading config.yaml:", e)
        sys.exit(1)
    
    repo_config = config.get("repository", {})
    interactive_loop(repo_config)