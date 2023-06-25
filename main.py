from pyswip import Prolog
import tkinter as tk
from PIL import Image, ImageTk

tempBombList = []

# Convert coordinates(x,y) to indexes
def get_cell_index(x, y, num_cols):
    return ((x - 1) * num_cols) + y

def query_prolog(window, height, width):
    for i in range(len(tempBombList)):
        variable_list = tempBombList[i].get().split(",")
        x = variable_list[0]
        y = variable_list[1]
        print(x, y)
        cell_indices = get_cell_index(int(x), int(y), int(width.get()))
        tempBombList[i] = cell_indices
    count = 0
    bombsList = []
    for i in range(height.get()):
        for y in range(width.get()):
            count += 1
            if count == 1 and (count in tempBombList):
                bombsList.append('-1')
            elif count == 1:
                bombsList.append('1')
            elif count in tempBombList:
                bombsList.append('#')
            else:
                bombsList.append('0')
    bombsList = ','.join(bombsList)
    bombsList = f"[{bombsList}]"

    # Create a Prolog object
    prolog = Prolog()

    # Load and consult the Prolog knowledge base
    prolog.consult('dominoes.pl')
    print("search(%s, %s, %s, Solution)." % (bombsList, height.get(), width.get()))
    # Query Prolog using PySWF
    query_result = list(prolog.query("search(%s, %s, %s, Solution)." % (bombsList, height.get(), width.get())))
    result = []
    count = 1
    for i in query_result[0]['Solution']:
        if i == 1:
            result.append(count)
        count += 1

    # Process the query result and update the GUI accordingly
    count = 0
    completed = []
    for i in range(height.get()):
        for y in range(width.get()):
            print("Result", result)
            count += 1
            if count in completed:
                continue
            if count in tempBombList:
                print("if")
                bombImg = ImageTk.PhotoImage(Image.open("Bomb.gif").resize((100, 80)))
                cell = tk.Button(window, image=bombImg, bg="white", fg="black", width=100, height=80)
                cell.image = bombImg
                cell.grid(row=8 + i, column=1 + y)
            else:
                print("else")
                cell = tk.Button(window, bg="white", fg="black", text=" ", width=14, height=5)
                cell.grid(row=8 + i, column=1 + y)
                # for z in range(len(result)):
                #     if count in result[z]:
                if count + 1 in result:
                    dominoImg = ImageTk.PhotoImage(Image.open("DominoHorizontal.gif").resize((208, 80)))
                    cell = tk.Button(window, image=dominoImg, bg="white", fg="black", width=208, height=80)
                    cell.image = dominoImg
                    cell.grid(row=8 + i, column=1 + y, columnspan=2)  # Resize the image to fit in two columns
                    completed.append(count)
                    completed.append(count + 1)
                    result = []
                elif count + width.get() in result:
                    dominoImg = ImageTk.PhotoImage(Image.open("DominoVertical.gif").resize((100, 165)))
                    cell = tk.Button(window, image=dominoImg, bg="white", fg="black", width=100, height=165)
                    cell.image = dominoImg
                    cell.grid(row=8 + i, column=1 + y, rowspan=2)  # Resize the image to fit in two rows
                    completed.append(count)
                    completed.append(count + width.get())
                    result = []
                # break


def getBombPositions(bombsNum, window, height, width):
    # Create bomb input fields dynamically based on number of bombs
    for i in range(bombsNum.get()):
        bomb_label = tk.Label(window, text="Bomb Position " + str(i + 1) + ": ")
        bomb_label.grid(row=3, column=i * 2, padx=5, pady=5)
        bomb_input = tk.Entry(window, width=15)
        bomb_input.grid(row=3, column=i * 2 + 1, padx=5, pady=5)
        tempBombList.append(bomb_input)

    # Bind the query_prolog() function to a button click event or any other event as needed
    button = tk.Button(window, fg="black", bg="red", text="Create board",
                       command=lambda: query_prolog(window, height, width))
    button.grid(row=4, column=1, columnspan=3, padx=10, pady=10)


def create_gui():
    window = tk.Tk()
    window.title("Dominoes Game")
    window.geometry("720x480")

    # Create GUI widgets such as buttons, labels, etc.
    boardHeight = tk.Label(window, text="Board Height : ")
    boardHeight.grid(row=0, column=0, padx=10, pady=10)
    height = tk.IntVar()
    heightInput = tk.Entry(window, textvariable=height, width=15)
    heightInput.grid(row=0, column=1, padx=7, pady=10)

    boardWidth = tk.Label(window, text="Board Width : ")
    boardWidth.grid(row=1, column=0, padx=10, pady=10)
    width = tk.IntVar()
    widthInput = tk.Entry(window, textvariable=width, width=15)
    widthInput.grid(row=1, column=1, padx=7, pady=10)

    bombsNum = tk.Label(window, text="Number of bombs: ")
    bombsNum.grid(row=2, column=0, padx=10, pady=10)
    bombsNum = tk.IntVar()
    bombsNumInput = tk.Entry(window, textvariable=bombsNum, width=15)
    bombsNumInput.grid(row=2, column=1, padx=7, pady=10)

    button = tk.Button(window, fg="white", bg="black", text="OK",
                    command=lambda: getBombPositions(bombsNum, window, height, width))  # Use lambda to pass arguments
    button.grid(row=2, column=2, padx=10, pady=10)

    # run the app
    window.mainloop()


# Call the create_gui() function to start the GUI application
create_gui()
