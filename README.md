# Dropbox

### What is Dropbox

This dropbox system consists of a Client (scanner) and a Server system, each
designated a directory to maintain. The scanner will scan its directory at set
time intervals (default 5s) and detects if a file has been edited. It would then
establish a connection to the server and send changes in files.

The server would receive change requests, and carry them out. For the duration
where both server and client are running, changes in the client directory is
synchronised across the server directory.

Due to time constraint there are several areas of the dropbox system that can be
improved on. Details are included below.

### How to Run Dropbox

You can run both client and server from a single file using the command
```buildoutcfg
    python3 run.py
```
This will create a single thread to run the server instance and a single thread
to run the client instance. The default directories for client and server are
`dir/client` and `dir/server` respectively. You can specify other
directories by adding the `--cdir` and `--sdir` flags. Directories will be
created at the given paths if none exist.

Alternatively you can run the client and server individually from two terminal
instances by running `python3 start_server` and `python3 start_scanner`
separately.

**Note: This project was created on MacOS, and is currently untested on Windows.**

### Areas of Improvement

As this project was completed in ~8 hours over a Saturday, there are several
areas that can be improved upon. These are planned as future updates, to be
completed when time permits.
1. **Update Queuing**
   1. Currently if the scanner loses connection to the server, any file updates
   during this  period of time is lost. A synchronisation function can be added
   to the scanner to verify that file versions are consistent across client and
   server when connection is established. The client could queue failed requests
   in the meantime.
   2. Update queue could be processed to only push the most recent update for
   each file. Though currently the scanner interval is quite short, and files
   are unlikely to be changed multiple times per interval.
2. **Multiple Server Endpoints**
   1. Currently only a single file could be updated to the server at once, this
   could be problematic if a significant number of files were changed within a
   single scanner interval, potentially even leading updates to be dropped.
   Future expansions could add more endpoints to allow for more updates to be
   executed concurrently.
   2. Alternatively the update queueing in the previous section could be used to
   store requests not completed within a single scanner interval.
3. **Improved Update Granularity**
   1. Currently if a file is edited in any way, it is updated on the server in
   its entirety. This can be inefficient, especially if many small changes are
   made in a short interval of time. A future development would be to only
   update changes within a file. Potentially via keeping an existing copy of
   local files, making comparisons when changes are detected and only sending
   changes to the server.
4. **Improved Authentication**
   1. More stringent authentication could be implemented i.e. token systems,
   which could protect the server better than a static authentication key stored
   in the system settings.