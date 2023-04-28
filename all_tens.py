import itertools
import multiprocessing
import sys

def num_combinations(nums: list) -> set:
    # Generate all possible permutations of the input numbers (4!)
    singles = set(itertools.permutations(nums))
  
    return singles

def get_operations(nums: list) -> list:
    # *10+ operation is used to pair numbers together.
    # for example the digits 1 2 -> 1*10+2 -> 12
    operators = ['+', '-', '*', '/', '*10+']
    expressions = []
    
    for i in range(2, len(nums) + 1):
        expressions.append(list(itertools.product(operators, repeat=i)))
    return expressions

def get_ordered_expressions(nums: list) -> list:
    operations = get_operations(nums)
    expressions = []
  
    if len(nums) == 2:
        for op in operations[0]:
            expressions.append(f'{nums[0]}{op[0]}{nums[1]}')
  
    if len(nums) == 3:
        for op in operations[1]:
            expressions.append(f'{nums[0]}{op[0]}{nums[1]}{op[1]}{nums[2]}')
            expressions.append(f'({nums[0]}{op[0]}{nums[1]}){op[1]}{nums[2]}')
            expressions.append(f'{nums[0]}{op[0]}({nums[1]}{op[1]}{nums[2]})')

    if len(nums) == 4:
        for op in operations[2]:
            expressions.append(f'{nums[0]}{op[0]}{nums[1]}{op[1]}{nums[2]}{op[2]}{nums[3]}')
            expressions.append(f'({nums[0]}{op[0]}{nums[1]}{op[1]}{nums[2]}){op[2]}{nums[3]}')
            expressions.append(f'{nums[0]}{op[0]}({nums[1]}{op[1]}{nums[2]}{op[2]}{nums[3]})')
            expressions.append(f'({nums[0]}{op[0]}{nums[1]}){op[1]}{nums[2]}{op[2]}{nums[3]}')
            expressions.append(f'{nums[0]}{op[0]}({nums[1]}{op[1]}{nums[2]}){op[2]}{nums[3]}')
            expressions.append(f'{nums[0]}{op[0]}{nums[1]}{op[1]}({nums[2]}{op[2]}{nums[3]})')
            expressions.append(f'({nums[0]}{op[0]}{nums[1]}){op[1]}({nums[2]}{op[2]}{nums[3]})')
    return expressions

def solve_all_tens(nums: list, analyze=False):
    # Check if each expression evaluates to 1 through 10 and print the unique expressions for each result
    results = {}
    nums = num_combinations(nums)
    num_expressions = 0
    
    numPossibilities = {}
    for i in range(1, 11):
        numPossibilities[i] = 0
    
    # start with single digit expressions 
    for perm in nums:
        perm = list(perm)
        exprs = get_ordered_expressions(perm)
        num_expressions += len(exprs)
        for expr in exprs:
            # Evaluate expression and check if it equals the target number
            try:
                res = round(eval(expr), 2)
                if res in range(1, 11):
                    if res not in results:
                        results[int(res)] = expr
                    numPossibilities[int(res)] += 1
            except ZeroDivisionError:
                continue
            if len(results) == 10 and not analyze:
                return True, results
    return False, results, numPossibilities, num_expressions

# Produce all possible combinations of 4 numbers from 1 to 9,
# Attempt to solve each combination, and count the number of solvable and unsolvable problems

def solve_chunk(nums):
    solvable = 0
    unsolvable = 0
    for num in nums:
        solved = solve_all_tens(num)
        if solved[0]:
            solvable += 1
        else:
            unsolvable += 1
    return solvable, unsolvable

def count_solvable_combinations_parallel():
    # Determine the number of available CPU cores
    num_processes = multiprocessing.cpu_count()
    
    # Split the set of number combinations into smaller chunks based on the number of processes
    num_combinations = itertools.combinations_with_replacement(range(1, 10), 4)
    
    def chunks(l, n):
        for i in range(0, n):
            yield l[i::n]

    # Create a separate process to solve each chunk
    pool = multiprocessing.Pool(processes=num_processes)
    resl = pool.map(solve_chunk, chunks(list(num_combinations), num_processes))
    solvable = 0
    unsolvable = 0
    for res in resl:
        solvable += res[0]
        unsolvable += res[1]
        
    print(f'Unsolvable: {unsolvable}, Solvable: {solvable}')
    


if __name__ == '__main__':    
    nums = [int(num) for num in sys.argv[1:]]
    
    if(len(nums) == 4):
        solved, results, possibilities, num_expressions = solve_all_tens(nums, analyze=True)
        
        p = sum(possibilities.values())

        for key, val in sorted(results.items()):
            percentage = round((possibilities[key]/(num_expressions - possibilities[key])*100), 2)
            print(f'{val}  = {str(key)} ({possibilities[key]} possibilities, {percentage}% of total)')

        print(f'{p} total valid possibilities in {num_expressions} expressions ({round((p/(num_expressions - p)*100), 2)}%)')
    else:
        count_solvable_combinations_parallel()

"""
# Unsolvable: 119, Solvable: 376


# Test the solution for all problems provided by beast academy.

# Note they have 313 problems in total, but the earlier test suggests there are actually 375...

# So maybe an issue in the code (rounding error?) or the problems are not all unique (duplicates)

# Code all seems to be in dist/v8.25.0/bundle_allten.js
# ./src/util/ProblemUtil.ts (contains the problems by day)
PROBLEMS_BY_DAY = ["1126", "1225", "1255", "4479", "4445", "2557", "4489", "2268", "1299", "2277", "4679", "2367", "1247", "3467", "3346",
                   "3578", "2667", "2399", "2269", "1278", "1135", "3679", "4689", "3447", "1145", "1227", "2777", "1279", "1357", "1249",
                   "3455", "2778", "2578", "1789", "2377", "3399", "1337", "4568", "2238", "4458", "1344", "1335", "3566", "3799", "1458",
                   "2299", "2458", "2333", "1229", "1138", "2227", "1445", "1348", "3368", "3478", "1446", "4468", "1257", "2344", "3559",
                   "1379", "3479", "3379", "3389", "1116", "2256", "2588", "2288", "1267", "1358", "1349", "1146", "2688", "2677", "1457",
                   "2248", "3357", "1459", "3466", "2456", "1779", "2356", "3335", "3569", "2258", "3359", "2666", "1269", "2788", "2566",
                   "4466", "1237", "3446", "3489", "3469", "3789", "2559", "2488", "1488", "2668", "2467", "1338", "2466", "3358", "2289",
                   "2388", "3579", "2556", "1226", "1557", "1799", "2469", "2267", "1139", "3445", "2999", "2336", "1688", "5568", "1266",
                   "3668", "1236", "2378", "2468", "3699", "2479", "2234", "1277", "1368", "2278", "2339", "1235", "3458", "1136", "2569",
                   "3388", "4467", "2499", "4448", "1228", "2459", "3468", "2577", "1668", "2669", "2589", "1579", "1469", "1468", "1466",
                   "2247", "2359", "1133", "4669", "3567", "2455", "2337", "1256", "2335", "5689", "2266", "1288", "1156", "1245", "3345",
                   "3488", "2366", "2349", "1566", "2244", "3448", "3366", "2899", "2699", "2678", "5556", "2446", "1233", "1369", "1455",
                   "2233", "5567", "1356", "3556", "1223", "1124", "1244", "5578", "4446", "3348", "3369", "2347", "3349", "1123", "3456",
                   "2889", "2338", "4668", "2237", "3689", "1114", "1137", "1568", "1238", "4488", "1222", "1333", "2558", "3333", "2389",
                   "1248", "4478", "1144", "2259", "1345", "2478", "1115", "1346", "3557", "2357", "2235", "1259", "2255", "1355", "2249",
                   "1577", "2369", "3555", "1246", "2568", "4688", "4578", "2489", "5667", "1567", "1268", "3339", "1479", "2449", "3344",
                   "4567", "1448", "1234", "1336", "2224", "2555", "3367", "2448", "2358", "2799", "2334", "2379", "1359", "1367", "2229",
                   "1366", "3558", "2346", "2345", "3355", "3449", "2368", "2236", "1339", "2457", "3337", "1239", "1678", "4566", "2567",
                   "2245", "1134", "1467", "5677", "4456", "3338", "4588", "3336", "2579", "2789", "2599", "2447", "2689", "2279", "2223",
                   "1289", "2444", "3677", "4556", "2679", "1224", "5679", "1125", "2239", "3589", "3678", "2226", "1258", "3334", "1456",
                   "2888", "2225", "2228", "2477", "2246", "2779", "3356", "3378", "2355", "2445", "2348", "4469", "4457"]
unsolvable = 0
solvable = 0

for p in PROBLEMS_BY_DAY:
    p = [int(p[0]), int(p[1]), int(p[2]), int(p[3])]
    
    solved, results = solve_all_tens(p)
    
    if not solved:
        unsolvable += 1
    else:
        solvable += 1

print(f'Unsolvable: {unsolvable}, Solvable: {solvable}')
# Unsolvable: 0, Solvable: 313
"""