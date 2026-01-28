import arcade
from menu import MenuView

def main():
    window = arcade.Window(1024, 768, "Danger Monsters")
    window.show_view(MenuView())
    arcade.run()

if __name__ == "__main__":
    main()
    #Постарался сделать код как можно чище (предполагаю что нужны были комменатрии)