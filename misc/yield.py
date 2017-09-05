#!/usr/bin/env python

def test_yield(n):
    i = 0
    while i < n:
        '''
            make this function be a generator, so it's iterable
            once it touch the 'yield', return the yield obj
        '''
        yield i ** 2
        i += 1

def main():
    """docstring for main"""
    for i in test_yield(5):
        print(i)

    # generator doesn't have attr next() in python3
    test = test_yield(5)
    print(test.__class__)
    print(test.next())
    print(test.next())
    print(test.next())
    print(test.next())
    print(test.next())

if __name__ == '__main__':
    main()
