#!/usr/bin/env python
import argparse
from os import path

SUPPORT_OPERATER = ['withdraw', 'deposit', 'inquiry']

class Account(object):
    """docstring for Account"""
    _log_type = ['withdraw', 'deposit', 'inquiry', 'create account']

    def __init__(self, name, balance):
        super(Account, self).__init__()
        if not isinstance(name, str):
            raise ValueError
        self._name = name
        self._logname = self._name + '.txt'
        # load balance
        self._load_balance(balance)

    def withdraw(self, value):
        assert value>=0, 'value cannot be less than 0'
        if self._balance - value < 0:
            print("Your don't have enough money in your account for withdrawing.")
        else:
            self._balance -= value
            self._log(0, value)
            print("Operation Success!!\nYour balance: {0}".format(self._read_balance()))

    def deposit(self, value):
        assert value>=0, 'value cannot be less than 0'
        self._balance += value
        self._log(1, value)
        print("Operation Success!!\nYour balance: {0}".format(self._read_balance()))

    def inquiry(self, val=0):
        data = self._read_db()
        print('Account history:\n\t{0:<15} {1:<10} {2:<10} {3}'.format(
            'operation', 'value', 'balance', 'timestamp'))
        # only read last ten transactions
        if len(data) > 10:
            data = data[-10:]

        for line in data:
            if len(line)< 5:
                continue
            info = line.split(',')
            print('\t{0:<15} {1:<10} {2:<10} {3}'.format(info[0], info[1], info[2], info[3]))

        self._log(2)
    def _account_info(self):
        return '\tName   : {0:<15}\n\tBalance: {1}'.format(self._name, self._read_balance())

    def _load_balance(self, balance):
        if self._check_db():
            data = self._read_db()
            while len(data[-1])<4:
                data = data[:-1]
            data = data[-1].split(',')
            if len(data) > 3:
                line = data[-2].strip()

                if isnumber(line):
                    print("Load account success.")
                    self._balance = float(line)
                    print(self._account_info())

            if not hasattr(self, '_balance'):
                from sys import exit
                print("Load account fail, please remove {0} first.".format(self._logname))
                exit(-1)

        else:
            # create a new account
            assert isnumber(balance), "Create account fail, balance must be a number"
            self._balance = float(balance)
            print("Create account:\n{0}".format(self._account_info()))
            self._log(3, value=self._name)

    def _read_balance(self):
        return self._balance

    def _read_db(self):
        if self._check_db():
            with open(self._db_path(), 'r+') as fp:
                return fp.read().split('\n')[:-1]

    def _check_db(self):
        if path.exists(self._db_path()):
            self._hasdb = 1
        else:
            self._hasdb = 0
        return self._hasdb

    def _log(self, log, value=0):
        from datetime import datetime as dt
        if self._check_db():
            mode = 'a+'
        else:
            mode = 'w+'
        with open(self._db_path(), mode) as fp:
            fp.write('{0:<15},{1:<10},{2:<10},{3}\n'.format(
                self._log_type[log], value, self._read_balance(),dt.now()))

    def _db_path(self):
        dir_name = path.dirname(__file__)
        file_path = path.join(dir_name, self._logname)
        return file_path

def isnumber(value):
    try:
        float(value)
        return True
    except:
        return False

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w','--withdraw', nargs='?', metavar='withdraw', default=None)
    parser.add_argument('-d','--deposit',  nargs='?', metavar='deposit', default=None)
    parser.add_argument('-i', '--inquiry', nargs='?', metavar='inquiry', default=None)
    parser.add_argument('-b', '--balance', nargs='?', metavar='balance', default=None)
    parser.add_argument('name', nargs='?', default=None, type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arg()
    assert args.name!=None, 'Must has a account name'
    if args.balance is not None:
        assert isnumber(args.balance), "Balance must be a number"
        args.balance = float(args.balance)
    myacc = Account(args.name, args.balance)

    for operator in SUPPORT_OPERATER:
        val = getattr(args, operator)
        if val is not None:
            # check input first
            assert isnumber(val), "Must be a number"
            val = float(val)
            if operator != 'inquiry':
                print("{0:<10}: {1}".format(operator, val))
            method = getattr(myacc, operator)
            method(val)
