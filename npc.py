npc_folder_location = "content/albert.npc"
npc_talk_distance = 150


class NPC:
    def __init__(self) -> None:
        self.name = "Albert"
        self.npc_file = npc_folder_location

    def talk(self, distance):
        if distance < npc_talk_distance:
            file = open(self.npc_file, "r")
            data = file.read()
            file.close()
            lines = data.split("\n")
            print(lines)
        else:
            self.show_massage("Come closer..")

    def show_massage(self, text):
        print(f"{self.name}: {text}")
