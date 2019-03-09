for i in range(len(SNAKE_X) - 1): #Subtract 1 as there is nothing ahead of the head
            #Index backward
            index = len(SNAKE_X) - i - 1 # subtract 1 as len is 1 based
            print(index, i)
            #Move the previous body segment to the segment ahead of it
            SNAKE_X[index] = SNAKE_X[index - 1]
            SNAKE_Y[index] = SNAKE_Y[index - 1]