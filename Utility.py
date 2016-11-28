from microbit import *

grid=[[0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]]

x=2
y=2

def gridToImage(grid):
    tx = ""
    for x in grid:
        for y in x:
            tx+=str(y)
        tx+=":"
    return tx
            
            
while True:
    grid[x][y] = 9          
    display.show(Image(gridToImage(grid)))       
    sleep(100)
    

