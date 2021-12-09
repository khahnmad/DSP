import numpy as np

matrix = np.array([[0,.75,0,.25],
          [(1/3),0,(1/6),0.5],
          [0,0,1,0],
          [0,.25,.5,.25]])

matrix_2 = np.array([[0.25,.5,0,.25],[1/8,0.25,0.25,3/8],[0,0,1,0],[0.5,0,0.25,.25]])

print('hello')
first = np.matmul(matrix, matrix)
print(np.matmul(first, matrix))
# multiplication = matrix_2*matrix_2*matrix_2
# for row in list(multiplication):
#     print(row)


check = (1/4 * 0.203125) + (1/4 * 0.23958333) + (1/4 * 0)+ (1/4 * 0.09895833)
print(check)
another = 1/4 + (3/4 * 1/2) + (3/4 * 1/3 * 1/4)
print(another)
p_hat = np.array([[0,.75,0,.25],
          [(1/3),0,(1/6),0.5],
          [0,0,1,0],
          [0,0,0,1]])

empty_list = [np.matmul(p_hat, p_hat)]
for i in range(50):
    product = np.matmul(empty_list[-1], p_hat)
    empty_list.append(product)
    if i == 10:
        print(i)
        print(product)
        print()
    if i == 25:
        print(i)
        print(product)
        print()
print('fineal')
print(empty_list[-1])

game = np.array([[0,(1/6),(1/6),0.5,(1/6)],[0,0,0,(5/6),(1/6)],[0,0,0,(5/6),(1/6)],[0,0,0,1,0],[0,0,0,0,1]])
