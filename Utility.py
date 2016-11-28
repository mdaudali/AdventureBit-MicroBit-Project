from microbit import *

grid=[[0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]]

x=2
y=2

def Draw(grid):
    tx = ""
    for x in grid:
        for y in x:
            tx+=str(y)
        tx+=":"
    display.show(Image(tx))
            
            
while True:
    grid[x][y] = 9          
    Draw(grid)     
    sleep(100)
    

