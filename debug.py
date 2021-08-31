from gameclass import GT

class debug(GT):
    def save(self):
        super().save("debug.smc")

if __name__ == "__main__":
    with open("Vanilla.smc", "rb") as game:
        test = debug(game.read())
        test.Grabbables(object_by_object=True)
        test.save()
