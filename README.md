[homepage](https://github.com/n3k0fi5t/)
# this is the repo record what I had learned in python
- when I learned something, I will update this repo

<img src="https://i.imgur.com/2tStxFL.jpg" width="47%" height="47%">


---
- [**Some small projects**](#projects)
> 1. [chat server and client](#tcp)

> 2. [ptt crawler](#crawler)


- [**technique**](#technique)

## technique
[misc](https://github.com/n3k0fi5t/pythonLearn/tree/master/misc)
- misc thing in this folder


[decorator](https://github.com/n3k0fi5t/pythonLearn/tree/master/decorator)
- runtime and runtime limitation decorator


[progressor bar](https://github.com/n3k0fi5t/pythonLearn/tree/master/progressor_bar)
- As title, is the progressor bar


[global_updater](https://github.com/n3k0fi5t/pythonLearn/tree/master/global_updater)
- make module in other folder could be include in main and using
```python
globals().update()
```
to update functions in the module scope

## selenium
- google map

  - [CommentSearcher](https://github.com/n3k0fi5t/pythonLearn/blob/master/googlemap.py)

    [video](https://www.youtube.com/watch?v=S_FoFEcidPk)

  - [CommentSearcher-multi-thread ver](https://github.com/n3k0fi5t/pythonLearn/blob/master/googlemap_multi-thread.py)

    [video](https://www.youtube.com/watch?v=8z35_sE7B2E)

---

## projects
### tcp
[server](https://github.com/n3k0fi5t/pythonLearn/blob/master/tcp_chat_server.py)
- A chat server using limited threads which are dynamic assigned for each client, and a thread
to listen the connection.

[client](https://github.com/n3k0fi5t/pythonLearn/blob/master/simple_client.py)
- A chat client using two thread. one of threads is used to handle sending connection between server and the client, another is used for receiving.

![image](https://github.com/n3k0fi5t/pythonLearn/blob/master/sample_picture/chat2.png)


### crawler
[ptt_crawler](https://github.com/n3k0fi5t/pythonLearn/blob/master/ptt_crawler.py)
![image](https://github.com/n3k0fi5t/pythonLearn/blob/master/sample_picture/crawler.png)
- A ptt crawler crawle the web side ptt context.

  Functionality:

    crawle a specify account push comments in hot topics/given topic

    crawle a specify account posts in hot topics/given topic

[instagram_crawler](https://github.com/n3k0fi5t/pythonLearn/blob/master/instagram/instagram.py)
![image](https://github.com/n3k0fi5t/pythonLearn/blob/master/sample_picture/instagram_demo.png)
- [Base on instagram private api](https://github.com/ping/instagram_private_api)

  Emulate a simple instagram application

