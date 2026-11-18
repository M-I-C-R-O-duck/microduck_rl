import mujoco

class MicroDuckEnv:

    def __int__(self):
        pass

    def load_xml(self):
        self.model = mujoco.MjModel.from_xml_path("robot.xml") # TODO: need the actual .xml path
        self.data = mujoco.MjData(self.model)



def main():
    pass # TODO:

if __name__ == "__main__":
    main()