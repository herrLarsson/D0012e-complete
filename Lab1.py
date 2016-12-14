import random
import math
import time

def insertsort(unsorted_list):
    A = unsorted_list
    for i in range(1,len(A)):
        key = A[i]
        j = i - 1
        while j>=0 and A[j]>key :
            A[j+1] = A[j]
            j = j - 1
        A[j+1] = key
    return A


def b_insertsort(unsorted_list):
    A = unsorted_list
    for i in range(1,len(A)):
        key = A[i]              
        lo = 0                  
        hi = i                  
        while lo < hi:          
            mid = int(math.floor((hi+lo)/2))
            if A[mid] >= key:                   
                hi = mid                        
            else:
                lo = mid + 1    
        A.pop(i)                
        A.insert(hi,key)        
    return A

#marges 2 lists, generates sorted list
def merge(sorted_list_A, sorted_list_B):
    A = sorted_list_A                   
    B = sorted_list_B                   
    sorted_list = []                    
    while len(A) > 0 and len(B) > 0:    
        if A[0] <= B[0]:                
            sorted_list.append(A[0])   
            A.pop(0)                   
        else:
            sorted_list.append(B[0])
            B.pop(0)
    if len(A) != 0:                 
        sorted_list.extend(A)           
    else:                               
        sorted_list.extend(B)           
    return sorted_list                  


#merges all the sorted sublists into 1 final_list
def merge_sublists(sorted_sublists):
    while len(sorted_sublists)!=1:  
        sorted_sublists.append(merge(sorted_sublists[0],sorted_sublists[1]))
        sorted_sublists = sorted_sublists[2:]                               
    return sorted_sublists[0]


#generates the random values used in the list
def generate_random_list(size):
    inputList = []
    for i in range(0, size):
        inputList.append(random.randint(1, 10000))
    return inputList

#splits the initial list in half while the length of the list is longer than k
def split(unsorted_list, k):
    alist_withsublists = []
    alist_withsublists.append(list(unsorted_list))
    while len(alist_withsublists[0]) > k:
        hi = len(alist_withsublists[0])
        mid = int(math.floor((hi)/2))       
        alist_withsublists.append(alist_withsublists[0][:mid])
        alist_withsublists.append(alist_withsublists[0][mid:])
        alist_withsublists = alist_withsublists[1:]
    return alist_withsublists


#count execution time and calls all the relevant functions
def mergesort(unsorted_list, k, algo):
    time1 = time.time()                  
    b = split(unsorted_list, k)             
    final_list = []                         
      
    for x in range(0, len(b)):                  
        final_list.append(algo(b[x]))        

    final_list = merge_sublists(final_list)         
    time2 = time.time()                     
    sort = time2 - time1                 
    print len(final_list), ';', k, ';', sort                   
    


def run_test(unsorted_list, k, k_step, n_step, algo):
    n = len(unsorted_list)
    while n > 0 and k > 0:
        mergesort(unsorted_list[:n], k, algo)
        k = k - k_step
        n = n - n_step

def main():
    n = 100
    k = 10
    k_step = 0
    n_step = 1
    unsorted_list = generate_random_list(n)
    print "n=", n," k=", k," k_step=", k_step, " n_step", n_step
    print 'n; k ; b_insertsort'
    run_test(list(unsorted_list), k, k_step, n_step, b_insertsort)
    print 'n; k ; ', 'insertsort'
    run_test(list(unsorted_list), k, k_step, n_step, insertsort)


main()
