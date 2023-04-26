# All Tens

A simple solver for the all tens challenge found at https://beastacademy.com/all-ten written in python.

Example use:

```
time python3 all_tens.py 1 2 3 4
2+3-1*4 = 1
2+3+1-4 = 2
2+(3+1)/4 = 3
2-3+1+4 = 4
2/(3-1)+4 = 5
1+4-2+3 = 6
1+(4-2)*3 = 7
2+3-1+4 = 8
2+3+1*4 = 9
2+3+1+4 = 10
python3 all_tens.py 1 2 3 4  0.07s user 0.03s system 87% cpu 0.108 total
```

By not specifying 4 args, it will run all possible combinations of 4 digits 1-9, and will simply print the number of solvable and unsolvable solutions.