import json
import random
import time

#code = '1_100_1000_1'
#code = '1_200_1000_1'
#code = '1_500_1000_1'
#code = '1_1000_1000_1'
code = '1_2000_1000_1'
#code = '1_5000_1000_1'

# Ler dados de entrada
def read_weights_and_costs(file_name='instances/knapPI_' + code):
    count = 1
    weights = {}
    costs = {}
    ratio = {}
    
    file = open(file_name, "r")
    data = file.readlines()
    
    number_of_things = int(data[0].split()[0])
    capacity = int(data[0].split()[1])
    

    for i in range(1, number_of_things + 1):
        
        costs[count] = int(data[i].split()[0])
        weights[count] = int(data[i].split()[1])
        ratio[count] = costs[count]/weights[count]
        count = count + 1

    return weights, costs, ratio, number_of_things, capacity


# Criar solução candidata
def create_new_solution(num_of_things, weights, costs, n_solution, n_weight, n_cost, item_to_remove):
    t_weight = n_weight
    t_cost = n_cost
    rc = number_of_things
 
    #print(n_solution)
    list_of_things = list(range(1, rc+1))  
    # Remover todos os itens da solução inicial, da lista de itens fora da mochila
    for item in n_solution:
        list_of_things.remove(item)
        rc = rc - 1

    # Remover um item da mochila e atualiza o custo e o peso
    n_solution.remove(item_to_remove)
    t_weight = t_weight - weights[item_to_remove]
    t_cost = t_cost - costs[item_to_remove]

    # inserir elementos na mochila enquanto ela suportar
    while(t_weight <= capacity):
        random_thing_index = random.randint(0, rc-1)
        random_item = list_of_things[random_thing_index]

        n_solution.append(random_item)
        list_of_things.remove(random_item)
        t_weight = t_weight + weights[random_item]
        t_cost = t_cost + costs[random_item]

        rc = rc - 1

    # O último item inserido na mochila(dentro do loop) faz seu peso ultrapassar a capacidade
    # Por isso é preciso remove-lo
    if t_weight > capacity:
        n_solution.remove(random_item)
        t_weight = t_weight - weights[random_item]
        t_cost = t_cost - costs[random_item]
        
    return n_solution, t_weight, t_cost
    

def LOCALSEARCH(num_of_things, weights, costs, new_solution, new_weight, new_cost):
    #print('local', new_solution)
    best_neigh = list(new_solution)
    best_weight = new_weight
    best_cost = new_cost
    
    for item_to_remove in new_solution:
        #print(initial_solution, item)
        n_solution = list(new_solution)
        #print(new_solution)
        #new_solution.remove(item)
        #print(new_solution)
        n_solution, n_weight, n_cost = create_new_solution(num_of_things, weights, costs, n_solution, new_weight, new_cost, item_to_remove)
        
        #print('SOL: ', new_solution)
        #print('WEI: ', t_weight)
        #print('COS: ', t_cost)
        
        if n_cost > best_cost:
            #print('entry 1')
            #print(best_neigh, TABU)
                #print('entry 2')
            best_neigh = n_solution
            best_weight = n_weight
            best_cost = n_cost
            
    #print('BEST: ', best_neigh)
    #print('BEST: ', best_weight)
    #print('BEST: ', best_cost)
    #print('best', best_neigh)
    return best_neigh, best_weight, best_cost
        
def construct_solution(number_of_things, weights, costs, ratio):
    total_weight = 0
    total_cost = 0
   
    solution = []
    list_of_things = list(range(1, number_of_things+1))
    
    # inserir elementos na mochila enquanto ela suportar
    while(total_weight <= capacity):
        alpha = random.random()
        min_cost = ratio[min(ratio, key=ratio.get)]
        max_cost = ratio[max(ratio, key=ratio.get)]
        threeshould_of_RCL = min_cost + alpha*(max_cost - min_cost)
        RCL = []
        
        for item in list_of_things:
            if ratio[item]>threeshould_of_RCL:
                RCL.append(item)
        #print('RCL', RCL)  
        rc = len(RCL)
        
        if rc != 0:
            random_thing_index = random.randint(0, rc-1)
            random_item = RCL[random_thing_index]

            # Inserir item na mochila, e remover da lista de itens fora da mochila
            solution.append(random_item)
            list_of_things.remove(random_item)
            # Atualizar o peso e o custo atual
            total_weight = total_weight + weights[random_item]
            total_cost = total_cost + costs[random_item]

            rc = rc - 1
    
    # O último item inserido na mochila(dentro do loop) faz seu peso ultrapassar a capacidade
    # Por isso é preciso remove-lo
    if total_weight > capacity:
        solution.remove(random_item)

        total_weight = total_weight - weights[random_item]
        total_cost = total_cost - costs[random_item]
    print('this works')
    return solution, total_weight, total_cost
    
    
    
    
def GRASP(num_of_things, weights, costs, ratio):

    k = 0 # iteração sem mudança na solução
    LIST_OF_SOLUTIONS = []
    LIST_OF_BEST = []
    LIST_AFTER_LS = []
    
    best_solution = None
    best_solution_cost = None
    best_solution_weight = None
    
    #LIST_OF_SOLUTIONS.append(initial_cost)
    #LIST_OF_BEST.append(best_solution_cost)
    

    #TABU = [-1] * tabu_size
    #tabu_ind = 0
    
    # Itera enquanto a solução não melhorar em k iterações
    while k < number_iterations_solution_is_not_improved:
        # Conjunto de soluções vizinhas locais a serem exploradas


        # Gera solução candidata
        new_solution, new_weight, new_cost = construct_solution(num_of_things, weights, costs, ratio)
        LIST_OF_SOLUTIONS.append(new_cost)
        new_solution, new_weight, new_cost = LOCALSEARCH(num_of_things, weights, costs, new_solution, new_weight, new_cost)
        LIST_AFTER_LS.append(new_cost)
        #new_solution.sort()
        # A melhor solução vizinha não deve estar na lista TABU (testada anteriormente)
        #if new_solution not in TABU:
        #TABU[tabu_ind] = new_solution
        #tabu_ind = (tabu_ind + 1)%tabu_size
        
        
        
        
        if best_solution_cost == None or new_cost > best_solution_cost:
            best_solution = new_solution
            best_solution_cost = new_cost
            best_solution_weight = new_weight
            k = 0
        else:
            k = k + 1  
            
        #initial_solution = list(new_solution)
        #initial_cost = new_cost
        #initial_weight = new_weight
            
        print('Best Solution Cost --> ', best_solution_cost, 'k: ', k)
        
                
        
        LIST_OF_BEST.append(best_solution_cost)
        
    record_solutions(solutions=LIST_OF_SOLUTIONS, after_ls=LIST_AFTER_LS, best=LIST_OF_BEST, suf='_solution.csv')
    #record_solutions(solutions=LIST_OF_BEST, suf='_best.csv')

    return best_solution, best_solution_weight, best_solution_cost
 
# Gravar soluções em arquivo
def record_solutions(solutions, after_ls, best, suf, code=code):
        with open('saidas/GP/' + code  + suf, 'a') as file:
            file.write('Constructed;AfterLS;Best\n')
            
            for item1, item2, item3 in zip(solutions, after_ls, best):
                file.write(str(item1) + ';' + str(item2) + ';' + str(item3) + '\n')
                

if __name__ == '__main__':
    
    start = time.time()
    
    number_iterations_solution_is_not_improved = 100
    #size_of_tabu = 20

    weights, costs, ratio, number_of_things, capacity = read_weights_and_costs()
    #print(weights)
    #print(costs)
    #print(ratio)
    
    
    #initial_solution, initial_weight, initial_cost = create_solution(weights, costs, number_of_things, capacity)
    
    #print('FIRST SOLUTION', initial_solution, initial_weight, initial_cost, capacity)
    
    
    final_solution, final_weight, final_cost = GRASP(number_of_things, weights, costs, ratio)
    
    print(final_solution)
    final = time.time()
    
    print('Final Solution: ', final_solution, '\nCost: ', final_cost, '\nWeight', final_weight)
    print('Time: ', final-start)
    
    
            
    
    
    
    
    
    