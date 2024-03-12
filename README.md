
# Veeam Test Task

Python application that synchronizes two folders: source and replica.


## Authors

- [@Hoai Vu Nguyen](https://github.com/hvnsoft)


![Logo](https://avatars.githubusercontent.com/u/156953199?v=4)



## Key Features

- Synchronization is one-way. The replica folder is modified to exactly match content of the source folder;

- Synchronization is performed periodically.

- File operations are logged to a log file and to the console output.

- Folder paths, synchronization interval and log file path can be provided using the command line arguments.



## 🛠 Technology Used
Python



## How to start

To start this app, open a console in the root directory (in the folder where main.py located) and run the following command
```bash
  python main.py [-s] ['source_folder_path'] [-r] ['replica_folder_path'] [-l] ['log_file_path'] [-i] [interval_time]
```

For example:
```bash
  python main.py -s 'E:/source' -r 'D:/replica' -l 'sync.log' -i 10
```

```bash
  python main.py
```