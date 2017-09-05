[homepage](https://github.com/n3k0fi5t/)
# this is the repo record what I had learned in python
- when I learned something, I will update this repo

---
- [**Some small projects**](#projects)
> 1. [chat server and client](#tcp)

> 2. [ptt crawler](#crawler)

- [**technique**](#technique)

## technique
[misc](https://github.com/n3k0fi5t/pythonLearn/tree/master/misc)
```
misc thing in this folder
```

[decorator](https://github.com/n3k0fi5t/pythonLearn/tree/master/decorator)
```
runtime and runtime limitation decorator
```

[progressor bar](https://github.com/n3k0fi5t/pythonLearn/tree/master/progressor_bar)
```
As title, is the progressor bar
```

[global_updater](https://github.com/n3k0fi5t/pythonLearn/tree/master/global_updater)
```
make module in other folder could be include in main
and using
```
>```py
globals()
``` to update functions in this module scope



---

## projects
### tcp
[server](https://github.com/n3k0fi5t/pythonLearn/blob/master/tcp_chat_server.py)
```
A chat server using limited threads which are dynamic assigned for each client, and a thread
to listen the connection.
```
[client](https://github.com/n3k0fi5t/pythonLearn/blob/master/simple_client.py)
```
A chat client using two thread. one of threads is used to handle sending connection between server and the client,
another is used for receiving.
```

### crawler
```
A ptt crawler crawle the web side ptt context.
Functionality:
  crawle a specify account push comments in hot topics/given topic
  crawle a specify account posts in hot topics/given topic
```
[ptt_crawler](https://github.com/n3k0fi5t/pythonLearn/blob/master/ptt_crawler.py)
