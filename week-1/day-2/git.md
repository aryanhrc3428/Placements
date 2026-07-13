# Git Command Reference Manual: Ultimate Mastery Guide

Welcome to the comprehensive reference manual for Git. This document details the use case, mechanics, and concrete command-line examples for **every single command** exposed by the system-wide execution tree.

---

## 1. Main Porcelain Commands
High-level user commands used for everyday source code management, branching, and repository interaction.

### `add`
* **Use Case:** Stages modifications in the working directory to the index (staging area) preparing them for the next commit.
* **Example:**
    ```bash
    git add src/main.py
    ```

### `am`
* **Use Case:** Applies a series of patches from an email mailbox format (`mbox`), typically used to integrate changes sent via mailing lists.
* **Example:**
    ```bash
    git am incoming-patches.mbox
    ```

### `archive`
* **Use Case:** Packages a specific tree structure or commit version into a clean compressed archive file (e.g., ZIP or TAR), excluding Git metadata.
* **Example:**
    ```bash
    git archive --format=zip HEAD > release-v1.zip
    ```

### `backfill`
* **Use Case:** Automatically downloads missing partial clone objects on-demand when historical references are requested.
* **Example:**
    ```bash
    git backfill --deepen=10
    ```

### `bisect`
* **Use Case:** Employs a binary search algorithm across commit history to rapidly isolate which specific commit introduced a bug or regression.
* **Example:**
    ```bash
    git bisect start
    git bisect bad                 # Current commit is broken
    git bisect good v2.0.0         # Last known stable version
    ```

### `branch`
* **Use Case:** Manages development paths. Used to list active branches, create new local tracks, or delete old feature paths.
* **Example:**
    ```bash
    git branch feature/authentication
    ```

### `bundle`
* **Use Case:** Packages references and objects into a single file container to transfer revisions offline or without an active network connection.
* **Example:**
    ```bash
    git bundle create repository.bundle main
    ```

### `checkout`
* **Use Case:** Switches context between branches or restores files in the working tree back to their last committed state.
* **Example:**
    ```bash
    git checkout develop
    ```

### `cherry-pick`
* **Use Case:** Extracts a specific commit from one branch and applies it directly onto the current checked-out branch as a new commit.
* **Example:**
    ```bash
    git cherry-pick e4a2b91c
    ```

### `citool`
* **Use Case:** Launches a graphical window dedicated to staging files, writing messages, and completing commits without using the CLI.
* **Example:**
    ```bash
    git citool
    ```

### `clean`
* **Use Case:** Purges untracked files and directories from the local working directory to ensure a pristine codebase state.
* **Example:**
    ```bash
    git clean -fd
    ```

### `clone`
* **Use Case:** Copies a remote repository structure down into a brand new local directory path, establishing remote tracking branches.
* **Example:**
    ```bash
    git clone [https://github.com/user/project.git](https://github.com/user/project.git)
    ```

### `commit`
* **Use Case:** Takes a snapshot of the staged changes in the index and commits it to the repository history with a descriptive log message.
* **Example:**
    ```bash
    git commit -m "feat: implement security layer"
    ```

### `describe`
* **Use Case:** Generates a human-readable name for a given commit by finding the closest reachable tag and appending commit details.
* **Example:**
    ```bash
    git describe --tags
    ```

### `diff`
* **Use Case:** Displays line-by-line differences between files in the working directory, the staging index, or between two explicit commits.
* **Example:**
    ```bash
    git diff HEAD~1 HEAD
    ```

### `fetch`
* **Use Case:** Downloads references, commits, and objects from a remote repository without merging them into your local workspace branches.
* **Example:**
    ```bash
    git fetch origin
    ```

### `format-patch`
* **Use Case:** Converts individual local commits into individual `.patch` files formatted ready to be submitted via email tracking.
* **Example:**
    ```bash
    git format-patch main..feature-branch
    ```

### `gc`
* **Use Case:** Runs the internal Garbage Collector to pack references, compress object files, and clean up dead history blocks.
* **Example:**
    ```bash
    git gc --prune=now
    ```

### `gitk`
* **Use Case:** Opens a traditional Tcl/Tk graphical engine to visually explore histories, branches, merges, and code updates.
* **Example:**
    ```bash
    gitk --all
    ```

### `grep`
* **Use Case:** Searches through tracked project files for lines matching a regular expression pattern, ignoring untracked assets.
* **Example:**
    ```bash
    git grep "TODO: auth_fix"
    ```

### `gui`
* **Use Case:** Starts a lightweight graphical program allowing developers to execute merges, commits, updates, and stages visually.
* **Example:**
    ```bash
    git gui
    ```

### `history`
* **Use Case:** An experimental tool used to perform deep history rewrites, restructuring sequences of commits systematically.
* **Example:**
    ```bash
    git history rewrite --filter-branch
    ```

### `init`
* **Use Case:** Initializes a brand new, empty local Git repository or converts an existing unversioned directory structure.
* **Example:**
    ```bash
    git init
    ```

### `log`
* **Use Case:** Displays a chronological timeline of commits made to the current branch, complete with author, date, and messages.
* **Example:**
    ```bash
    git log --oneline --graph --all
    ```

### `maintenance`
* **Use Case:** Registers the current repository for periodic automated optimization tasks like background pre-fetching and object packing.
* **Example:**
    ```bash
    git maintenance start
    ```

### `merge`
* **Use Case:** Combines independent development histories together by integrating commits from a target branch into the current one.
* **Example:**
    ```bash
    git merge feature/billing
    ```

### `mv`
* **Use Case:** Moves or renames a tracked file, directory, or symlink, automatically staging the change for the next commit.
* **Example:**
    ```bash
    git mv old_name.py new_name.py
    ```

### `notes`
* **Use Case:** Appends supplementary context metadata notes to a commit object without modifying the commit's content or SHA-1 hash signature.
* **Example:**
    ```bash
    git notes add -m "Reviewed by security team"
    ```

### `pull`
* **Use Case:** Fetches updates from a remote tracking branch and immediately incorporates them into the current checked-out local branch.
* **Example:**
    ```bash
    git pull origin main
    ```

### `push`
* **Use Case:** Uploads your local branch commits and references up to a remote repository database, updating the remote tracking state.
* **Example:**
    ```bash
    git push origin feature/ui-refresh
    ```

### `range-diff`
* **Use Case:** Compares two distinct commit ranges (such as two different iterations of a rebased feature branch) to audit changes.
* **Example:**
    ```bash
    git range-diff main..v1 main..v2
    ```

### `rebase`
* **Use Case:** Re-applies local commits on top of a fresh upstream commit baseline tip, creating a linear project history.
* **Example:**
    ```bash
    git rebase main
    ```

### `reset`
* **Use Case:** Resets the current HEAD pointer, the staging index, or the working tree to a specified historical commit state.
* **Example:**
    ```bash
    git reset --hard HEAD~1
    ```

### `restore`
* **Use Case:** Discards unstaged modifications in local source files, reverting them back to the state of a specified commit or index reference.
* **Example:**
    ```bash
    git restore path/to/file.json
    ```

### `revert`
* **Use Case:** Safely records a brand new commit that explicitly undoes the changes introduced by an earlier bad commit.
* **Example:**
    ```bash
    git revert c3a1098b
    ```

### `rm`
* **Use Case:** Removes a file from the working tree directory and removes it from the index tracking system simultaneously.
* **Example:**
    ```bash
    git rm config.env
    ```

### `scalar`
* **Use Case:** Enforces performance configurations tailored specifically for extremely massive enterprise repositories.
* **Example:**
    ```bash
    scalar register
    ```

### `shortlog`
* **Use Case:** Summarizes `git log` output by grouping commits by author name, providing a clean overview of contributors.
* **Example:**
    ```bash
    git shortlog -s -n
    ```

### `show`
* **Use Case:** Outputs detailed context data regarding a specific commit, tag, tree, or file blob contents.
* **Example:**
    ```bash
    git show v1.0.4
    ```

### `sparse-checkout`
* **Use Case:** Configures the working directory to track and display only a specific subfolder pattern, optimizing monorepo workspaces.
* **Example:**
    ```bash
    git sparse-checkout set /src/backend
    ```

### `stash`
* **Use Case:** Temporarily saves dirty local workspace changes to an internal stack, reverting the directory back to a clean status.
* **Example:**
    ```bash
    git stash save "Work in progress - switching tasks"
    ```

### `status`
* **Use Case:** Displays a real-time summary of files that are untracked, modified but unstaged, or staged in the index ready for commit.
* **Example:**
    ```bash
    git status
    ```

### `submodule`
* **Use Case:** Embeds an entirely separate external Git repository inside a subfolder of the parent project repo.
* **Example:**
    ```bash
    git submodule add [https://github.com/vendor/lib.git](https://github.com/vendor/lib.git) extern/lib
    ```

### `survey`
* **Use Case:** An experimental metrics tool used to profile repository scale dimensions, sizes, and file weights.
* **Example:**
    ```bash
    git survey --dimensions
    ```

### `switch`
* **Use Case:** Explicitly focuses on switching context between existing branches to prevent overlapping options found in checkout.
* **Example:**
    ```bash
    git switch release/v2
    ```

### `tag`
* **Use Case:** Creates point-in-time reference markers tied to important historical snapshots (e.g., version releases).
* **Example:**
    ```bash
    git tag -a v2.0.0 -m "Production release 2.0"
    ```

### `worktree`
* **Use Case:** Enables checking out multiple active branches concurrently into entirely separate local folder directories.
* **Example:**
    ```bash
    git worktree add ../bugfix-directory hotfix/patch-1
    ```

---

## 2. Ancillary Commands / Manipulators
Utility commands used to manage the configuration, structure, and history tracking of a repository.

### `config`
* **Use Case:** Queries or assigns environment parameters, developer names, emails, and preferences across global or repository layers.
* **Example:**
    ```bash
    git config --global user.name "John Doe"
    ```

### `fast-export`
* **Use Case:** Exports the repository's commit history into a serialized stream file for migration into other systems or structures.
* **Example:**
    ```bash
    git fast-export --all > repo_dump.fi
    ```

### `fast-import`
* **Use Case:** Rapidly reads a serialized stream dump file to recreate repositories, branches, and commit histories on the fly.
* **Example:**
    ```bash
    git fast-import < repo_dump.fi
    ```

### `filter-branch`
* **Use Case:** Rewrites history by applying a filter across all historical commits (e.g., removing a committed secret key file).
* **Example:**
    ```bash
    git filter-branch --tree-filter 'rm -f passwords.txt' HEAD
    ```

### `mergetool`
* **Use Case:** Launches an external user-defined visual diff interface (e.g., Meld, KDiff3) to resolve complicated merge conflicts.
* **Example:**
    ```bash
    git mergetool
    ```

### `pack-refs`
* **Use Case:** Packs loose tracking references and branch heads into a single flat lookup file (`.git/packed-refs`) to save disk lookups.
* **Example:**
    ```bash
    git pack-refs --all
    ```

### `prune`
* **Use Case:** Deletes loose object files that no longer have any reachable connections from tags, branches, or logs.
* **Example:**
    ```bash
    git prune -v
    ```

### `reflog`
* **Use Case:** Maintains a complete local history tracking log recording exactly when branch heads changed or moved, allowing recovery of lost commits.
* **Example:**
    ```bash
    git reflog show main
    ```

### `refs`
* **Use Case:** Provides low-level administration controls over the repository references backend database engines.
* **Example:**
    ```bash
    git refs migrate --to=reftable
    ```

### `remote`
* **Use Case:** Manages the configuration URLs and tracking configurations tied to external hosting servers (e.g., origin).
* **Example:**
    ```bash
    git remote add upstream [https://github.com/original/repo.git](https://github.com/original/repo.git)
    ```

### `repack`
* **Use Case:** Groups loose object blobs into consolidated pack files to reduce storage footprints and optimize memory lookup speeds.
* **Example:**
    ```bash
    git repack -a -d
    ```

### `replace`
* **Use Case:** Dynamically replaces a specified target object inside the Git object graph with a separate proxy element without altering object signatures.
* **Example:**
    ```bash
    git replace a1b2c3d4 e5f6g7h8
    ```

---

## 3. Ancillary Commands / Interrogators
Tools designed to audit history, analyze data structures, check integrity, and extract diagnostic logs.

### `annotate`
* **Use Case:** Outputs file text line-by-line annotated with the commit details, author, and timestamp of the last modification.
* **Example:**
    ```bash
    git annotate source.cpp
    ```

### `blame`
* **Use Case:** Shows author and commit metadata for every line of a target file, typically used to find when a line was introduced.
* **Example:**
    ```bash
    git blame -L 10,25 utility.go
    ```

### `bugreport`
* **Use Case:** Gathers local OS information, build contexts, shell profiles, and Git version details into a text diagnostic report for bug filing.
* **Example:**
    ```bash
    git bugreport --output-directory=~/Desktop
    ```

### `count-objects`
* **Use Case:** Scans the database and displays the count of loose objects vs packed objects along with their corresponding disk footprints.
* **Example:**
    ```bash
    git count-objects -v
    ```

### `diagnose`
* **Use Case:** Creates a zipped diagnostic bundle of the current repository containing structural attributes, configurations, and internal parameters.
* **Example:**
    ```bash
    git diagnose
    ```

### `difftool`
* **Use Case:** Routes differences between commits or code ranges directly out into external side-by-side comparison software applications.
* **Example:**
    ```bash
    git difftool HEAD~1 HEAD --tool=vimdiff
    ```

### `fsck`
* **Use Case:** Audits the local object database system, verifying object connectivity graph health and reporting corrupted links or orphan objects.
* **Example:**
    ```bash
    git fsck --full --strict
    ```

### `gitweb`
* **Use Case:** Generates the runtime foundation requirements for a simple browser-based web frontend interface displaying local Git archives.
* **Example:**
    ```bash
    # Typically invoked by automated script wrappers or web servers
    gitweb.cgi
    ```

### `help`
* **Use Case:** Opens official documentation manuals for a requested Git command inside the terminal window or default system web browser.
* **Example:**
    ```bash
    git help rebase
    ```

### `instaweb`
* **Use Case:** Instantly provisions a localized web server hosting a browseable `gitweb` frontend mapping the current active project tree.
* **Example:**
    ```bash
    git instaweb --httpd=webrick --start
    ```

### `merge-tree`
* **Use Case:** Performs an in-memory 3-way merge test between two explicit trees without touching the active working directory files or index states.
* **Example:**
    ```bash
    git merge-tree branch-A branch-B
    ```

### `rerere`
* **Use Case:** Automatically records how conflict sections are solved by the developer, matching and auto-applying those exact fixes in future merges.
* **Example:**
    ```bash
    git rerere clear
    ```

### `show-branch`
* **Use Case:** Displays a matrix summary of branches, illustrating the tracking paths and individual commit structures side by side.
* **Example:**
    ```bash
    git show-branch --all
    ```

### `verify-commit`
* **Use Case:** Validates the cryptographical GPG/SSH signatures appended to specific commit hashes, confirming identities.
* **Example:**
    ```bash
    git verify-commit e4a19b8
    ```

### `verify-tag`
* **Use Case:** Cryptographically validates the cryptographic verification strings bound inside signed release tags.
* **Example:**
    ```bash
    git verify-tag v1.0.0
    ```

### `version`
* **Use Case:** Outputs the system build signature version string representing the current running Git client installation framework.
* **Example:**
    ```bash
    git version
    ```

### `whatchanged`
* **Use Case:** A legacy log printer that provides a commit list while detailing what exact files changed along with their internal mode adjustments.
* **Example:**
    ```bash
    git whatchanged -n 5
    ```

---

## 4. Interacting with Others
Bridges used to connect, migrate, synchronize, or exchange patches between Git and external version control setups or email workflows.

### `archimport`
* **Use Case:** Imports history, revisions, and directories from a GNU Arch project database setup into a clean Git branch structure.
* **Example:**
    ```bash
    git archimport archive/repo branch-target
    ```

### `cvsexportcommit`
* **Use Case:** Exports a specific individual Git commit signature back into an active check-out workspace tracking a legacy CVS repository structure.
* **Example:**
    ```bash
    git cvsexportcommit -v HEAD
    ```

### `cvsimport`
* **Use Case:** Scans and salvages historical records, author branches, and file tracks directly out of older CVS software configurations.
* **Example:**
    ```bash
    git cvsimport -d :pserver:anonymous@cvs.server:/cvsroot module
    ```

### `cvsserver`
* **Use Case:** Acts as an emulation server layer, allowing clients tracking projects via legacy CVS systems to interact with the Git database repository.
* **Example:**
    ```bash
    git cvsserver pserver
    ```

### `imap-send`
* **Use Case:** Uploads a generated patch set collection read from system standard input directly up into a remote IMAP mail client outbox folder.
* **Example:**
    ```bash
    git format-patch -1 --stdout | git imap-send
    ```

### `p4`
* **Use Case:** Manages bidirectional sync coordination structures linking active Perforce storage server nodes and local Git environments.
* **Example:**
    ```bash
    git p4 clone //depot/project@all local-folder
    ```

### `quiltimport`
* **Use Case:** Imports a structured series of Quilt patch set files sequentially, applying them step-by-step onto the current branch line.
* **Example:**
    ```bash
    git quiltimport --patches /path/to/patches
    ```

### `request-pull`
* **Use Case:** Summarizes the changes between a base commit and a branch, formatting it as a textual pull request template.
* **Example:**
    ```bash
    git request-pull v1.0 [https://github.com/user/project.git](https://github.com/user/project.git) main
    ```

### `send-email`
* **Use Case:** Transmits patches directly via an SMTP server configuration to maintainer mailing lists.
* **Example:**
    ```bash
    git send-email --to=devel@project.org *.patch
    ```

### `svn`
* **Use Case:** Operates a bidirectional bridge, allowing developers to use Git to pull from, push to, and branch against Subversion repositories.
* **Example:**
    ```bash
    git svn clone [http://svn.example.com/project/trunk](http://svn.example.com/project/trunk) -T trunk
    ```

---

## 5. Low-level Commands / Manipulators (Plumbing)
Low-level plumbing operations used to directly construct objects, modify references, and manage index file binaries.

### `apply`
* **Use Case:** Applies changes from a diff file directly to workspace files without recording a commit or updating tracking layers.
* **Example:**
    ```bash
    git apply internal-fix.patch
    ```

### `checkout-index`
* **Use Case:** Copies files directly out of the staged index binary storage registry and overwrites them onto the physical working tree directory.
* **Example:**
    ```bash
    git checkout-index -a -f
    ```

### `commit-graph`
* **Use Case:** Writes or validates a binary optimization file (`commit-graph`) that indexes commit relationships to speed up long history traversals.
* **Example:**
    ```bash
    git commit-graph write --reachable
    ```

### `commit-tree`
* **Use Case:** Generates a new raw commit object inside the database referencing an explicit tree SHA string and parent hashes.
* **Example:**
    ```bash
    git commit-tree 4a2b3c... -m "Plumbing commit example"
    ```

### `hash-object`
* **Use Case:** Computes the unique Git SHA-1 hash identifier for a local file target, optionally creating a new blob object in the database.
* **Example:**
    ```bash
    git hash-object -w document.txt
    ```

### `index-pack`
* **Use Case:** Parses an incoming pack archive file stream, computes hash indexes for every contained object, and outputs a matching index file (`.idx`).
* **Example:**
    ```bash
    git index-pack incoming-archive.pack
    ```

### `merge-file`
* **Use Case:** Performs a localized three-way file merge between three file arguments (base, mine, yours), writing the outputs inline.
* **Example:**
    ```bash
    git merge-file local.txt base.txt remote.txt
    ```

### `merge-index`
* **Use Case:** Scans the staged index file registry lookups and executes specific resolution script targets for items requiring conflict resolution.
* **Example:**
    ```bash
    git merge-index git-merge-one-file -a
    ```

### `mktag`
* **Use Case:** Creates an annotated tag object wrapper validation block by reading data directly from standard input streams.
* **Example:**
    ```bash
    git mktag < tag_definition_payload.txt
    ```

### `mktree`
* **Use Case:** Constructs a physical directory tree object inside the database using text formatting definitions provided via standard input.
* **Example:**
    ```bash
    git mktree < raw_tree_lines.txt
    ```

### `multi-pack-index`
* **Use Case:** Creates a centralized, global indexing directory mapping across multiple discrete pack files to optimize read latencies.
* **Example:**
    ```bash
    git multi-pack-index write
    ```

### `pack-objects`
* **Use Case:** Packs distinct object blobs into a compressed `.pack` archive file based on explicit object list criteria read from standard input.
* **Example:**
    ```bash
    git pack-objects pack_name < target_objects_list.txt
    ```

### `prune-packed`
* **Use Case:** Scans local data files and purges loose object files whose copies already exist safely inside integrated consolidated pack files.
* **Example:**
    ```bash
    git prune-packed
    ```

### `read-tree`
* **Use Case:** Reads structural directory tree metadata records directly into the active staging index, preparing for commit construction.
* **Example:**
    ```bash
    git read-tree 3a9c7b2...
    ```

### `replay`
* **Use Case:** An experimental plumbing tool that replays a commit range on top of a new base, designed to run quickly in bare repositories.
* **Example:**
    ```bash
    git replay --onto new-base old-tip
    ```

### `symbolic-ref`
* **Use Case:** Reads, manipulates, or clears symbolic reference links (such as mapping where `HEAD` points to).
* **Example:**
    ```bash
    git symbolic-ref HEAD refs/heads/develop
    ```

### `unpack-objects`
* **Use Case:** Explodes compressed object content blocks out of a `.pack` archive file and extracts them into individual loose object files.
* **Example:**
    ```bash
    git unpack-objects < archive.pack
    ```

### `update-index`
* **Use Case:** Directly registers working tree file changes into the staged index file binary framework, bypassing standard `git add` behavior.
* **Example:**
    ```bash
    git update-index --assume-unchanged secrets.json
    ```

### `update-ref`
* **Use Case:** Updates the SHA-1 value stored in a specific reference path (like a branch head) safely, avoiding race conditions.
* **Example:**
    ```bash
    git update-ref refs/heads/main a4b3c2...
    ```

### `write-tree`
* **Use Case:** Generates a reusable directory tree object inside the database from the current contents of the staged index.
* **Example:**
    ```bash
    git write-tree
    ```

---

## 6. Low-level Commands / Interrogators
Plumbing inspection operations used to verify file layers, audit references, and query raw data properties.

### `cat-file`
* **Use Case:** Outputs the raw text contents, object sizes, or type attributes of any database object by its SHA hash value.
* **Example:**
    ```bash
    git cat-file -p e4a3b19
    ```

### `cherry`
* **Use Case:** Compares a local branch against an upstream branch to find commits that have not yet been integrated or merged.
* **Example:**
    ```bash
    git cherry v1.0-release feature-track
    ```

### `diff-files`
* **Use Case:** Compares the structural state of raw files in the current working directory against the staged index file registry.
* **Example:**
    ```bash
    git diff-files --name-only
    ```

### `diff-index`
* **Use Case:** Compares a specified database tree object directly against the active staging index or local working tree files.
* **Example:**
    ```bash
    git diff-index HEAD
    ```

### `diff-pairs`
* **Use Case:** Performs raw content and file mode comparisons between two provided tracking blobs.
* **Example:**
    ```bash
    git diff-pairs blob_sha1 blob_sha2
    ```

### `diff-tree`
* **Use Case:** Compares the structural file additions, modifications, or deletions between two separate database tree objects.
* **Example:**
    ```bash
    git diff-tree tree_sha1 tree_sha2
    ```

### `for-each-ref`
* **Use Case:** Iterates over all repository tracking references, outputting formatted details based on a custom layout template string.
* **Example:**
    ```bash
    git for-each-ref --format='%(refname) %(authorname)' refs/heads/
    ```

### `for-each-repo`
* **Use Case:** Iterates across a list of repository paths stored in your configuration and runs a specified Git command inside each directory.
* **Example:**
    ```bash
    git for-each-repo --config=maintenance.repo maintenance run
    ```

### `get-tar-commit-id`
* **Use Case:** Extracts the embedded Git commit SHA string out of an archive file that was previously created using `git archive`.
* **Example:**
    ```bash
    git get-tar-commit-id < package.tar
    ```

### `last-modified`
* **Use Case:** An experimental tool that queries historical records to determine when specific files were last modified.
* **Example:**
    ```bash
    git last-modified source.py
    ```

### `ls-files`
* **Use Case:** Lists every file tracked in the active staging index, along with file statuses, cached elements, and unmerged targets.
* **Example:**
    ```bash
    git ls-files --stage
    ```

### `ls-remote`
* **Use Case:** Queries a remote repository server and lists all available branch references, tag heads, and commit signatures.
* **Example:**
    ```bash
    git ls-remote origin
    ```

### `ls-tree`
* **Use Case:** Lists the contents, mode metrics, object types, and SHA identifiers inside a specific database directory tree object.
* **Example:**
    ```bash
    git ls-tree HEAD --name-only
    ```

### `merge-base`
* **Use Case:** Finds the best common ancestor commit between two or more branches, helping locate split or merge divergence origins.
* **Example:**
    ```bash
    git merge-base develop feature-track
    ```

### `name-rev`
* **Use Case:** Finds symbolic reference names (like matching tags or branches) for a raw commit SHA-1 hash identifier.
* **Example:**
    ```bash
    git name-rev --name-only e4a3b1
    ```

### `pack-redundant`
* **Use Case:** Identifies redundant pack files whose object data is fully duplicated across other active pack files, helping save space.
* **Example:**
    ```bash
    git pack-redundant --all
    ```

### `repo`
* **Use Case:** Inspects internal repository states, metadata formats, and architecture parameters.
* **Example:**
    ```bash
    git repo --info
    ```

### `rev-list`
* **Use Case:** Lists commit object hashes in reverse chronological order based on selection parameters, used by higher-level scripts.
* **Example:**
    ```bash
    git rev-list --count HEAD
    ```

### `rev-parse`
* **Use Case:** Resolves user-facing reference parameters (like branch names, tags, or `HEAD~1`) into their absolute SHA-1 commit signatures.
* **Example:**
    ```bash
    git rev-parse main
    ```

### `show-index`
* **Use Case:** Decodes and displays the internal tracking indexing logs of a packed object `.idx` file mapping layout.
* **Example:**
    ```bash
    git show-index < .git/objects/pack/pack-xyz.idx
    ```

### `show-ref`
* **Use Case:** Lists all local references, tags, and branch heads alongside their corresponding SHA commit values.
* **Example:**
    ```bash
    git show-ref --tags
    ```

### `unpack-file`
* **Use Case:** Extracts the text contents of a raw database blob object and writes it out into a temporary file on disk.
* **Example:**
    ```bash
    git unpack-file blob_sha_string
    ```

### `var`
* **Use Case:** Outputs the value of Git logical environment variables (such as the default author signature identity).
* **Example:**
    ```bash
    git var GIT_AUTHOR_IDENT
    ```

### `verify-pack`
* **Use Case:** Validates packed Git archive pack files, ensuring object indexing and data hashes are structurally intact.
* **Example:**
    ```bash
    git verify-pack -v .git/objects/pack/pack-xyz.pack
    ```

---

## 7. Low-level Commands / Syncing Repositories
Low-level networking components used to transfer objects, protocol streams, and data payloads over the wire.

### `daemon`
* **Use Case:** Launches an unauthenticated, lightweight network server to share repositories via the Git wire protocol (`git://`).
* **Example:**
    ```bash
    git daemon --base-path=/srv/git --export-all
    ```

### `fetch-pack`
* **Use Case:** Lower-level plumbing counterpart to `fetch`. Receives missing compressed pack files and object lists from a remote server connection stream.
* **Example:**
    ```bash
    git fetch-pack origin refs/heads/main
    ```

### `http-backend`
* **Use Case:** Server-side CGI implementation of the Git network protocol over HTTP/HTTPS, enabling smart repository push and pull features.
* **Example:**
    ```bash
    # Typically declared inside web server routing engine files (Apache/NGINX)
    ScriptAlias /git/ /usr/libexec/git-core/git-http-backend/
    ```

### `send-pack`
* **Use Case:** Lower-level plumbing counterpart to `push`. Uploads local objects and updates remote references over a secure connection stream.
* **Example:**
    ```bash
    git send-pack origin refs/heads/feature-branch
    ```

### `update-server-info`
* **Use Case:** Generates auxiliary index documentation mapping metadata to help old or simple HTTP hosting servers serve repositories.
* **Example:**
    ```bash
    git update-server-info
    ```

---

## 8. Low-level Commands / Internal Helpers
Internal utility operations and fallback handlers used by higher-level Git commands or hook logic.

### `check-attr`
* **Use Case:** Evaluates the structural `.gitattributes` parameters active for a specific target path file string.
* **Example:**
    ```bash
    git check-attr -a path/to/source.js
    ```

### `check-ignore`
* **Use Case:** Debugs `.gitignore` exclude rules by showing which specific rule pattern is filtering or masking a targeted file path.
* **Example:**
    ```bash
    git check-ignore -v temp_logs/debug.log
    ```

### `check-mailmap`
* **Use Case:** Converts raw author names and email addresses to their canonical identities as defined in the project's `.mailmap` file.
* **Example:**
    ```bash
    git check-mailmap "old-email@domain.com"
    ```

### `check-ref-format`
* **Use Case:** Validates that a reference name string meets Git's naming conventions before attempting to create branches or tags.
* **Example:**
    ```bash
    git check-ref-format refs/heads/valid-name
    ```

### `column`
* **Use Case:** Formats incoming list data arrays into clean, aligned horizontal columns within the terminal interface.
* **Example:**
    ```bash
    git branch --list | git column --mode=column
    ```

### `credential`
* **Use Case:** Interacts with systemic background helpers to look up, register, or clear tracking username passwords and authentication tokens.
* **Example:**
    ```bash
    echo -e "protocol=https\nhost=github.com" | git credential fill
    ```

### `credential-cache`
* **Use Case:** Stores passwords or tokens in system memory for a configurable duration, avoiding re-authentication prompts.
* **Example:**
    ```bash
    git config credential.helper 'cache --timeout=3600'
    ```

### `credential-store`
* **Use Case:** Saves login passwords and authentication tokens directly onto unencrypted flat files on disk.
* **Example:**
    ```bash
    git config credential.helper 'store --file=~/.my-credentials'
    ```

### `fmt-merge-msg`
* **Use Case:** Formats a clean commit summary description paragraph out of historical logs for an automated merge event.
* **Example:**
    ```bash
    git fmt-merge-msg < .git/FETCH_HEAD
    ```

### `hook`
* **Use Case:** Directly invokes specific automation hook scripts (e.g., `pre-commit`) via the configuration interface framework.
* **Example:**
    ```bash
    git hook run pre-commit
    ```

### `interpret-trailers`
* **Use Case:** Parses, modifies, or appends key-value metadata tags (like `Signed-off-by: `) to the end of a commit log text block.
* **Example:**
    ```bash
    git interpret-trailers --trailer "Signed-off-by: Jane Doe <j@d.com>" commit_msg.txt
    ```

### `mailinfo`
* **Use Case:** Extracts the commit description, author identity metadata, and clean patch lines directly out of a single email message file.
* **Example:**
    ```bash
    git mailinfo msg.txt patch.txt < incoming-email.eml
    ```

### `mailsplit`
* **Use Case:** Splits a unified UNIX `mbox` multi-email archive container file apart into individual chronological messages.
* **Example:**
    ```bash
    git mailsplit -ooutput_folder mailbox.mbox
    ```

### `merge-one-file`
* **Use Case:** Standard helper script that resolves conflicts for a single file during a merge run, invoked automatically by `merge-index`.
* **Example:**
    ```bash
    # System-level call target
    git merge-index git-merge-one-file file.txt
    ```

### `patch-id`
* **Use Case:** Generates a hash signature for a diff or patch, ignoring line number shifts, to identify identical changes across branches.
* **Example:**
    ```bash
    git diff HEAD~1 | git patch-id
    ```

### `sh-i18n`
* **Use Case:** Shell setup environment logic managing internationalization translations for Git shell script frameworks.
* **Example:**
    ```bash
    # Sourced inside core execution scripts
    . "$(git --exec-path)/git-sh-i18n"
    ```

### `sh-setup`
* **Use Case:** Standard Shell initialization setup logic providing common variables, error message helpers, and configuration definitions.
* **Example:**
    ```bash
    # Sourced internally by Git shell scripts
    . "$(git --exec-path)/git-sh-setup"
    ```

### `stripspace`
* **Use Case:** Cleans whitespace, removes trailing empty gaps, and filters comment lines out of text streams or commit templates.
* **Example:**
    ```bash
    git stripspace < unformatted_message.txt
    ```

---

## 9. User-facing Repository, Command, and File Interfaces
Structural reference frameworks that define configuration behavior, ignored files, custom hooks, and syntax rules.

### `attributes`
* **Use Case:** References the functional framework of `.gitattributes` used to control line endings (`crlf`), merge drivers, and file filtering.
* **Example:**
    ```bash
    # Checked via doc references or setting parameters
    git help attributes
    ```

### `cli`
* **Use Case:** References the standard guidelines, option conventions, parameter styling rules, and flag parsing formats used by Git's CLI.
* **Example:**
    ```bash
    git help cli
    ```

### `hooks`
* **Use Case:** References the automation script catalog configurations (e.g., `post-receive`, `pre-push`) triggered during repository operations.
* **Example:**
    ```bash
    git help hooks
    ```

### `ignore`
* **Use Case:** References the parsing logic and pattern syntax matching files and folders that should be skipped by project tracking systems.
* **Example:**
    ```bash
    git help ignore
    ```

### `mailmap`
* **Use Case:** References the syntax rules for mapping alternative name and email strings back to clear canonical user records.
* **Example:**
    ```bash
    git help mailmap
    ```

### `modules`
* **Use Case:** References the specification parameter schemas managing external submodules via the `.gitmodules` configuration file.
* **Example:**
    ```bash
    git help modules
    ```

### `repository-layout`
* **Use Case:** Details the explicit underlying internal structure, paths, and definitions inside the private `.git` directory container.
* **Example:**
    ```bash
    git help repository-layout
    ```

### `revisions`
* **Use Case:** References the extended matching syntax used to specify commit ranges, parent roots, and historical checkpoints (e.g., `HEAD@{3}`).
* **Example:**
    ```bash
    git help revisions
    ```

---

## 10. Developer-facing File Formats, Protocols, and Interfaces
Low-level wire protocol specifications, compression index definitions, and internal serialization specifications.

### `format-bundle`
* **Use Case:** References the internal underlying file format structure specifying how bundle files archive references and commits.
* **Example:**
    ```bash
    git help format-bundle
    ```

### `format-chunk`
* **Use Case:** Details the low-level layout schema for binary index chunks used by index-pack operations.
* **Example:**
    ```bash
    git help format-chunk
    ```

### `format-commit-graph`
* **Use Case:** References the structural definition schema defining how the `commit-graph` speed optimization map binary file is written.
* **Example:**
    ```bash
    git help format-commit-graph
    ```

### `format-index`
* **Use Case:** Details the binary layout and structural byte indexing specifications of the central `.git/index` staging area cache.
* **Example:**
    ```bash
    git help format-index
    ```

### `format-pack`
* **Use Case:** References the protocol specifications managing object packing delta compression structures inside `.pack` files.
* **Example:**
    ```bash
    git help format-pack
    ```

### `format-signature`
* **Use Case:** Details the data block storage formatting conventions used for inline cryptographic verification structures (GPG/SSH).
* **Example:**
    ```bash
    git help format-signature
    ```

### `protocol-capabilities`
* **Use Case:** Details the capability parameters exchanged between local client agents and remote servers during initial v0/v1 connections.
* **Example:**
    ```bash
    git help protocol-capabilities
    ```

### `protocol-common`
* **Use Case:** References the baseline transport variables, handshake structures, and parameter structures common across Git transport channels.
* **Example:**
    ```bash
    git help protocol-common
    ```

### `protocol-http`
* **Use Case:** Details the smart transfer request structures and payload streaming conventions used when operating Git actions over HTTP/HTTPS.
* **Example:**
    ```bash
    git help protocol-http
    ```

### `protocol-pack`
* **Use Case:** References the wire structures defining how packed archive object streams are packaged and pushed over the network.
* **Example:**
    ```bash
    git help protocol-pack
    ```

### `protocol-v2`
* **Use Case:** References the modernized layout version 2 network protocol architecture specification designed to speed up initial connection handshakes.
* **Example:**
    ```bash
    git help protocol-v2
    ```

---

## 11. External Commands
Independent helper applications, credential drivers, and large file optimization managers bundled into the environment runtime.

### `askpass`
* **Use Case:** Opens localized graphical popup pass-prompt windows to request user keys or passwords when running headlessly.
* **Example:**
    ```bash
    export GIT_ASKPASS=/path/to/askpass-helper
    ```

### `askyesno`
* **Use Case:** A Windows specific terminal prompt helper engine used to capture structural user validation input parameters.
* **Example:**
    ```bash
    # Internal component invoked by script logic loops
    ```

### `credential-helper-selector`
* **Use Case:** Launches an interactive selection prompt allowing developers to configure their desired active system credential manager engine.
* **Example:**
    ```bash
    git credential-helper-selector
    ```

### `credential-manager`
* **Use Case:** Launches the OS secure authentication framework system (e.g., Git Credential Manager) to protect access tokens via enterprise vaults.
* **Example:**
    ```bash
    git credential-manager core configure
    ```

### `lfs`
* **Use Case:** Extends Git to manage large media files, database objects, or binary graphics assets by substituting them with pointer files while storing the actual assets externally.
* **Example:**
    ```bash
    git lfs track "*.psd"
    ```

### `update-git-for-windows`
* **Use Case:** Connects to distribution nodes, audits local versions, and automates updates for the Git for Windows application suite tool chain.
* **Example:**
    ```bash
    git update-git-for-windows
    ```