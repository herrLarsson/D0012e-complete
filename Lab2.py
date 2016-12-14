import random
import csv
import sys
import time
#import winsound

def main(arguments):
    t = Test()
    test_loadfactor = False
    test_c = False
    test_size = False
    low = 0
    high = 0
    steps = 0

    if len(arguments) < 0:
        print 'there is something in the argument'
    # Remove first argument, it is a path to the script
    arguments.pop(0)
    while len(arguments) > 0:
        argument = arguments.pop(0)
        if argument == "-h":
            print "Welcome to lab2"
            print "This arguments exist"
            print "all      -   All algrithms are tested"
            print "linear   -   The linear probing algothm is tested"
            print "alt-linear-  The alt-linear probing algothm is tested"
            print "func_3   -  The func 3 probing algothm is tested"
            print "-s <int> -   Set size of hash list"
            print "-mv <int>-   Max value in keylist"
            print "-lf <int>-   Set loadfactor when all elemets from keylesi is inserted"
        elif argument == "all":
            t.linear = True
            t.alt_lin = True
            t.func_3 = True
        elif argument == "linear":
            t.linear = True
        elif argument == "alt-linear":
            t.alt_lin = True
        elif argument == "test-loadfactor":
            test_loadfactor = True
        elif argument == "test-c":
            test_c = True
        elif argument == "test-size":
            test_size = True
        elif argument == "func_3":
            t.func_3 = True
        elif argument == "-s":
            t.size = int(arguments.pop(0))
            t.max_value = t.size * 2 + 1000
        elif argument == "-mv":
            t.max_value = int(arguments.pop(0))
        elif argument == "-rd":
            t.rehash_depth = int(arguments.pop(0))
        elif argument == "-lf":
            t.load_factor = float(arguments.pop(0))
        elif argument == "-low":
            low = float(arguments.pop(0))
        elif argument == "-high":
            high = float(arguments.pop(0))
        elif argument == "-steps":
            steps = int(arguments.pop(0))
        elif argument == "-c":
            t.constant = int(arguments.pop(0))
        else:
            print "Invalid argument" + argument
            break
    if test_loadfactor and steps != 0:
        t.step_loadfactor(low, high, steps)
    elif test_c and steps != 0:
        t.step_c(low, high, steps)
    elif test_size and steps != 0:
        t.step_size(low, high, steps)
    else:
        t.run()
    if t.linear:
        csv_writer(t.results_lin, generate_filename("lin", t.load_factor, t.constant, t.size))
    if t.alt_lin:
        csv_writer(t.results_alt, generate_filename("alt", t.load_factor, t.constant, t.size))
    if t.func_3:
        csv_writer(t.results_cha, generate_filename("cha", t.load_factor, t.constant, t.size))
#  Freq = 400  # Set Frequency To 2500 Hertz
#   Dur = 250  # Set Duration To 1000 ms == 1 second
#    winsound.Beep(Freq, Dur)


class Test(object):
    linear = False
    alt_lin = False
    func_3 = False
    size = 0
    max_value = 100
    load_factor = 1.0
    constant = 5
    key_list = []
    fail_rehash = False
    rehash_depth = 5

    results_lin = [["Runtime(s)"], ["Hash counter"], ["Probe counter"], ["Collitions"], ["Longest collition chain"],
                   ["Size of hash list"], ["Load factor"], ["Key list size"]]
    results_alt = [["Runtime(s)"], ["Hash counter"], ["Probe counter"], ["Collitions"], ["Longest collition chain"],
                   ["Size of hash list"], ["Load factor"], ["Key list size"]]
    results_cha = [["Runtime(s)"], ["Hash counter"], ["Probe counter"], ["Collitions"], ["Longest collition chain"],
                   ["Rehash"], ["Size of hash list"], ["Load factor"], ["Constant"], ["Key list size"], ["Failed to rehash"]]

    def step_size(self, l, h, s):
        for i in range(0, s+1):
            step = (float(i) / float(s) * (h - l)) + l
            self.size = int(step)
            self.run()

    def step_c(self, l, h, s):
        for i in range(0, s+1):
            step = (float(i) / float(s) * (h - l)) + l
            self.constant = int(round(step))
            self.run()

    def step_loadfactor(self, l, h, s):
        for i in range(0, s+1):
            step = float((float(i) / float(s) * (h - l)) + l)
            self.load_factor = step
            self.run()

    def run(self):
        if self.linear or self.alt_lin or self.func_3:
            key_list_size = int(round(self.size * self.load_factor))
            if key_list_size != len(self.key_list):
                self.key_list = generate_key_list(key_list_size, self.max_value)
        else:
            print "No algorithms to run, use \"-h\" to see alternatives"
        if self.linear:
            hash_list1 = HashListLinear(self.size)
            time1 = time.time()
            for key_index in range(0, len(self.key_list)):
                hash_list1.insert(self.key_list[key_index])
            runtime = time.time() - time1

            self.results_lin[0].append(runtime)  # runtime
            self.results_lin[1].append(hash_list1.hash_counter)  # num of hash func
            self.results_lin[2].append(hash_list1.probe_counter)
            self.results_lin[3].append(hash_list1.num_insert_collision)
            self.results_lin[4].append(hash_list1.collisionChain)
            self.results_lin[5].append(len(hash_list1.hash_list))
            self.results_lin[6].append(self.load_factor)
            self.results_lin[7].append(key_list_size)
            print "One line linear"
        if self.alt_lin:
            hash_list2 = HashListAltLinear(self.size)

            time1 = time.time()
            for key_index in range(0, len(self.key_list)):
                key = self.key_list[key_index]
                hash_list2.insert(key)
            runtime = time.time() - time1
            self.results_alt[0].append(runtime)  # runtime
            self.results_alt[1].append(hash_list2.hash_counter)  # num of hash func
            self.results_alt[2].append(hash_list2.probe_counter)
            self.results_alt[3].append(hash_list2.num_insert_collision)
            self.results_alt[4].append(hash_list2.collisionChain)
            self.results_alt[5].append(len(hash_list2.hash_list))
            self.results_alt[6].append(self.load_factor)
            self.results_alt[7].append(key_list_size)
            print "One line alt"
        if self.func_3:
            hash_list3 = HashListF3(self.constant, self.size, self.rehash_depth)
            time1 = time.time()

            for key_index in range(0, len(self.key_list)):
                try:
                    hash_list3.insert(self.key_list[key_index])
                except RehashError as e:
                    self.fail_rehash = True

                    print "Failed to rehash: " + e.value
                    break
                pass
            keys_in_hash = 0
            for i in hash_list3.hash_list:
                if i is not None:
                    keys_in_hash += 1
            lf = float(keys_in_hash) / float(len(hash_list3.hash_list))
            # This could, and maybe should, be done in one line.
            runtime = time.time() - time1
            self.results_cha[0].append(runtime)  # runtime
            self.results_cha[1].append(hash_list3.hash_counter)  # num of hash func
            self.results_cha[2].append(hash_list3.probe_counter)
            self.results_cha[3].append(hash_list3.num_insert_collision)
            self.results_cha[4].append(hash_list3.collisionChain)
            self.results_cha[5].append(hash_list3.rehash_counter)
            self.results_cha[6].append(len(hash_list3.hash_list))

            self.results_cha[7].append(lf)
            self.results_cha[8].append(self.constant)
            self.results_cha[9].append(key_list_size)
            self.results_cha[10].append(self.fail_rehash)
            print "Added one line to printout mod 2"


def generate_key_list(size, max_value):
    step = int(round(max_value / size))
    return_list = []
    noise = 0
    for i in range(0, size):
        # add noise
        if step > 1:
            noise = random.randint(0, step - 1)
        i = int(round((float(i) / float(size)) * max_value)) + noise
        return_list.append(i)
    return return_list


def generate_list(size, object_to_repeat):
    l = object_to_repeat * size
    return l


def hash_func(key, size):
    hash_num = key % size
    return hash_num


def csv_writer(data, path):
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        for i in range(0, len(data[0])):
            to_write = []  # creates/resets list of items to write
            for line in data:
                to_write.append(line[i])  # Add item to the list
            writer.writerow(to_write)  # writes the row


def generate_filename(name, loadfactor, constant, size):
    times = time.strftime("%Y%m%d-%H%M%S")
    lf = ''
    s = ''
    c = ''
    if (loadfactor != 1.0):
        lf = '-lf=' + str(loadfactor)
    if (constant != 5):
        c = '-c=' + str(constant)
    if size != 100:
        s = '-s=' + str(size)
    name = times + name + lf + c + s + '.csv'
    return name


class HashListLinear(object):
    hash_list = []
    collisionChain = 0
    num_insert_collision = 0
    hash_counter = 0
    probe_counter = 0
    temp_collision_chain = 0

    def __init__(self, size):
        self.hash_list = generate_list(size, [None])

    def insert(self, key):
        hash_list = self.hash_list
        where_to_insert = hash_func(key, len(self.hash_list))
        self.hash_counter += 1
        if hash_list[where_to_insert] is not None:
            self.num_insert_collision += 1
            self.temp_collision_chain += 1  # counts the number of conflicts in chain
            where_to_insert = self.probing(where_to_insert)
            hash_list[where_to_insert] = key
        else:
            if self.temp_collision_chain > self.collisionChain:
                self.collisionChain = self.temp_collision_chain  # resets when chain is broken
            self.temp_collision_chain = 0
            hash_list[where_to_insert] = key

    def probing(self, hash_num):
        hash_list = self.hash_list
        for i in range(hash_num + 1, len(hash_list)):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        for i in range(0, hash_num):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        print "Linear : No free value in hashlist"


class HashListAltLinear(HashListLinear):
    g_up = []
    g_down = []

    def __init__(self, size):
        super(HashListAltLinear, self).__init__(size)
        self.g_up = generate_list(size, [0])
        self.g_down = generate_list(size, [0])

    def probing(self, hash_num):
        if self.g_up[hash_num] >= self.g_down[hash_num]:
            self.g_down[hash_num] += 1
            return self.f1_down(hash_num)
        else:
            self.g_up[hash_num] += 1
            return self.f2_up(hash_num)

    def f1_down(self, hash_num):
        hash_list = self.hash_list
        for i in range(hash_num + 1, len(hash_list)):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        for i in range(0, hash_num):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        print "f1 : No free value in hashlist"

    def f2_up(self, hash_num):
        hash_list = self.hash_list
        for i in range(hash_num - 1, 0, -1):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        for i in range(len(hash_list) - 1, hash_num + 1, -1):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        print "f2 : No free value in hashlist"


class HashListF3(HashListLinear):
    constant = 0
    rehash_counter = 0
    rehash_tries = 0

    def __init__(self, constant, size, rehash_depth):
        super(HashListF3, self).__init__(size)
        self.constant = constant
        self.rehash_depth = rehash_depth

    def insert(self, key):
        where_to_insert = hash_func(key, len(self.hash_list))
        self.hash_counter += 1
        if self.hash_list[where_to_insert] is None:
            if self.temp_collision_chain > self.collisionChain:
                self.collisionChain = self.temp_collision_chain  # resets when chain is broken
            self.temp_collision_chain = 0
            self.hash_list[where_to_insert] = key
        else:
            self.num_insert_collision += 1
            self.temp_collision_chain += 1  # counts the number of conflicts in chain

            try:
                where_to_insert = self.probing(where_to_insert, key)
            except Rehash:
                if self.rehash_tries < self.rehash_depth:
                    self.rehash_tries += 1
                    self.insert(key)
                else:
                    raise RehashError('Failed to input value, despite rehash')
            self.hash_list[where_to_insert] = key


    def probing(self, hash_num, key):
        j = self.linear_probing(hash_num)
        if abs(j - hash_num) <= self.constant:
            return j
        elif abs(j - hash_num) > self.constant:
            for i in range(hash_num, hash_num + self.constant + 1):
                if i >= len(self.hash_list): # Check if it overflowed
                    i = i - len(self.hash_list)
                if self.hash_list[i] is not None:
                    hy = hash_func(self.hash_list[i], len(self.hash_list))
                    if abs(j - hy)<= self.constant:
                        self.hash_list[j] = self.hash_list[i]
                        return i


        self.rehash_counter += 1
        self.rehash()
        raise Rehash('Done with rehash')


    def linear_probing(self, hash_num):
        hash_list = self.hash_list
        start = hash_num - self.constant
        if start < 0:
            start = len(hash_list) + start
        for i in range(start, len(hash_list)):
            self.probe_counter += 1
            if not hash_list[i]:
                return i
        for i in range(0, start - 1):
            self.probe_counter += 1
            if not hash_list[i]:
                return i

    def rehash(self):
        old_hash_list = self.hash_list
        self.hash_list = generate_list(len(old_hash_list), [None])
        for i in old_hash_list:
            if i is not None:
                self.insert(i)
        if old_hash_list == self.hash_list:
            raise RehashError('Same list as before')

class Rehash(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RehashError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
main(sys.argv)
