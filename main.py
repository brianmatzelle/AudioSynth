from bin import controller, EndScreenController

def main():
    synth = controller.Controller()
    synth.window.mainloop()
    print("Software Lead is: Brian Matzelle")
    print("Backend is: Kenechi Okoye ")
    print("Frontend is: Nicole Masciovecchio")
    start = EndScreenController.Controller(synth)
    start.mainLoop()

main()
