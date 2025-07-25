import datetime
import hashlib
import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional, Set, Type

HERE = Path(__file__).parent.resolve()


def check_submission() -> None:
    """Adapt me to individual games.

    (Remove the type: ignore comments once ellipses changed)
    """
    example_state = ...
    expected_choose_move_return_type = ...
    pickle_loader = ...
    # The type the pickled variable should be
    expected_pkl_type = ...
    # Check that the pickled variable can be used correctly
    pkl_checker_function = ...
    game_mechanics_hash = ...  # See below function

    return _check_submission(
        example_state=example_state,
        expected_choose_move_return_type=expected_choose_move_return_type,  # type: ignore
        expected_pkl_type=expected_pkl_type,  # type: ignore
        pkl_checker_function=pkl_checker_function,  # type: ignore
        pickle_loader=pickle_loader,  # type: ignore
        game_mechanics_hash=game_mechanics_hash,  # type: ignore
    )


def hash_game_mechanics() -> str:
    """Call me to generate game_mechanics_hash."""
    return sha256_file(HERE / "game_mechanics.py")


def get_local_imports(folder_path: Path = HERE) -> Set:
    """Get the names of all files imported from folder_path."""
    local_imports = set()
    for module in sys.modules.values():
        if not hasattr(module, "__file__") or module.__file__ is None:
            continue
        path = Path(module.__file__)
        # Module is in this folder
        if Path(os.path.commonprefix([folder_path, path])) == folder_path:
            local_imports.add(path.stem)
    return local_imports


def _check_submission(
    example_state: Any,
    expected_choose_move_return_type: Type,
    expected_pkl_type: Type,
    pkl_checker_function: Callable,
    game_mechanics_hash: str,
    pickle_loader: Optional[Callable[[str], Any]] = None,
) -> None:
    """Checks a user submission is valid.

    Args:
        example_state (any): Example of the argument to the user's choose_move function
        pickle_loader (Callable): If the user's choose_move takes a second argument of stored
                                  data (e.g. a value function), this is the function that loads
                                  it
    """
    assert hash_game_mechanics() == game_mechanics_hash, (
        "You've changed game_mechanics.py, please don't do this! :'( "
        "(if you can't escape this error message, reach out to us on slack)"
    )

    local_imports = get_local_imports()
    valid_local_imports = {"__main__", "game_mechanics", "check_submission"}
    assert local_imports.issubset(valid_local_imports), (
        f"You imported {local_imports - valid_local_imports}. "
        f"Please do not import local files other than "
        f"check_submission and game_mechanics into your main.py."
    )

    mains = [entry for entry in os.scandir(HERE) if entry.name == "main.py"]
    assert len(mains) == 1, "You need a main.py file!"
    main = mains[0]
    assert main.is_file(), "main.py isn't a Python file!"

    file_name = main.name.split(".py")[0]

    pre_import_time = datetime.datetime.now()
    mod = __import__(f"{file_name}", fromlist=["None"])
    time_to_import = (datetime.datetime.now() - pre_import_time).total_seconds()

    # Check importing takes a reasonable amount of time
    assert time_to_import < 2, (
        f"Your main.py file took {time_to_import} seconds to import.\n"
        f"This is much longer than expected.\n"
        f"Please make sure it's not running anything (training, testing etc) outside the "
        f"if __name__ == '__main__': at the bottom of the file"
    )

    # Check the choose_move() function exists
    try:
        choose_move = getattr(mod, "choose_move")
    except AttributeError as e:
        raise Exception(f"No function 'choose_move()' found in file {file_name}.py") from e

    # Check there is a TEAM_NAME attribute
    try:
        team_name = getattr(mod, "TEAM_NAME")
    except AttributeError as e:
        raise Exception(f"No TEAM_NAME found in file {file_name}.py") from e

    # Check TEAM_NAME isn't empty
    if len(team_name) == 0:
        raise ValueError(f"TEAM_NAME is empty in file {file_name}.py")

    # Check TEAM_NAME isn't still 'Team Name'
    if team_name == "Team Name":
        raise ValueError(
            f"TEAM_NAME='Team Name' which is what it starts as - "
            f"please change this in file {file_name}.py to your team name!"
        )

    if pickle_loader is not None:
        try:
            pkl_file = pickle_loader(team_name)
            assert isinstance(
                pkl_file, expected_pkl_type
            ), f"The .pkl file you saved is the wrong type! It should be a {expected_pkl_type}"
            pkl_checker_function(pkl_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Value dictionary file called 'dict_{team_name}.pkl' cannot be found! "
                f"Check the file exists & that the name matches."
            ) from e

    if pickle_loader is not None:
        action = choose_move(example_state, pkl_file)
    else:
        action = choose_move(example_state)

    assert isinstance(action, expected_choose_move_return_type), (
        f"Action output by `choose_move()` must be type {expected_choose_move_return_type}, "
        f"but instead {action} of type {type(action)} was output."
    )
    print(
        "Congratulations! Your Repl is ready to submit :)\n\n"
        f"It'll be using value function file called 'dict_{team_name}.pkl'"
    )


def sha256_file(filename: Path) -> str:
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        while n := f.readinto(mv):  # type: ignore
            h.update(mv[:n])
    return h.hexdigest()
