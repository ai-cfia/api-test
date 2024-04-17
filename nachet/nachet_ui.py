import time
import sys

from datastore import get_testing_image
from inference_testing import start_testing

CACHE = {
    "blob_image": {}
}


def test_image(seed: str):
    clear()
    print("Start loading images")
    seconds = time.perf_counter()

    if not CACHE.get("blob_image").get(seed):
        CACHE["blob_image"][seed] = get_testing_image(
            CACHE["testing_folders"][0],
            CACHE["DATASTORE_CLIENT"],
            seed,
        )

    print(f"Finish loading {len(CACHE['blob_image'][seed])} images")
    print(f"Took: {'{:10.4f}'.format(time.perf_counter() - seconds)} seconds")

    amount = input(
"""
Enter the number of image you want to test the models against:
"""
    )
    nb_image = int(amount)

    _ = input("Enter any key to start testing")

    start_testing(nb_image, CACHE["blob_image"][seed], CACHE["NACHET_BACKEND_URL"], CACHE["MODELS"])

    #actions[4](0)


def user_image(seed: str):
    clear()
    print(f"not implement yet {seed}")
    menu()

def folder_specific_image(seed: str):
    clear()
    print("not implement yet")
    menu()

def clear():
    sys.stdout.write("\033[H\033[J")

def menu(*args):
    if args:
        CACHE["seeds_name"] = args[0]
        CACHE["testing_folders"] = args[1]
        CACHE["MODELS"] = args[2]
        CACHE["DATASTORE_CLIENT"] = args[3]
        CACHE["NACHET_BACKEND_URL"] = args[4]

    print("Welcome to nachet testing app!")
    for i, seed in enumerate(CACHE["seeds_name"]):
        print(f"{i+1}. {seed}")

    selection = input("Select the seed you want to test:")

    seed_to_test = int(selection)-1

    clear()

    selection = input("""
To test with test picture enter 1.
To test with user picture enter 2.
To test with a pecific folder enter 3.
To exit quit the app enter 4.

Please enter your selection:
    """
    )
    actions[int(selection)](CACHE["seeds_name"][seed_to_test])

actions = {
    1: test_image,
    2: user_image,
    3: folder_specific_image,
    4: sys.exit,
    5: menu,
}
