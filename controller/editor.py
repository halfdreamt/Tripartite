class editor:
    def __init__(self, world):
        self.world = world

    # check if the given map location has an entity - if so, call entity editor function, if not, call world editor function
    def handleRightMouseClick(self, entity):
        if entity:
            self.handleEntityEditor(entity)
        else:
            self.handleWorldEditor()

    # handle entity editor
    def handleEntityEditor(self, entity):
        pass

    # handle world editor
    def handleWorldEditor(self):
        pass

