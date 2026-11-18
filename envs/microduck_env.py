import mujoco


def load_xml():
    model = mujoco.MjModel.from_xml_path("robot.xml")
    data = mujoco.Mjdata(model)

def main():
    print() # TODO:

if __name__ == "__main__":
    main()