#!/usr/bin/env python

def main():
    select = ["吃飯","洗澡","要我","eat","bath","me"]
    input_hint = "".join(["{}.{:<15}".format(idx,val) for idx,val in enumerate(select,1)])

    print("歐逆醬的挑戰")
    usr_input = input("歐逆醬~要先{}\n".format(input_hint))

    if usr_input not in [str(i) for i in range(1,len(select)+1)]:
        #find best match
        count = lambda sel, inp: sum([sum([1 if s==i else 0 for s in sel]) for i in inp])
        idx = [count(s,usr_input) for s in select]
        res = idx.index(max(idx))
    else:
        res = int(usr_input)-1

    print("Your choice is {}".format(select[res]))

if __name__ == '__main__':
    main()
