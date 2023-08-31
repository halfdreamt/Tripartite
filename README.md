# Tripartite

Tripartite is an ECS (Entity Component System) game engine designed to efficiently manage complicated world states with minimal graphical rendering for high performance. Initial data is loaded from JSON files in the REC directory. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame.

```bash
pip install pygame
```

## Usage

```python
python main.py
```

This will start the program. Press Continue to begin the simulation. Clicking on an entity will reveal its component data. Space pauses the simulation. Number keys 1-4 alter the speed. Navigate using middle mouse or WASD. Pressing escape will reveal the menu. Battle features are unfinished (menu button not functional).

The existing initial data will generate two wandering farmer entities, who will occasionally thirst for water and path-find to the spawned water pot entity. A simple example but the engine is designed for flexibility and scale.

<img width="1316" alt="Screenshot 2023-08-31 at 11 58 51 AM" src="https://github.com/halfdreamt/Tripartite/assets/31080937/085c5815-91e6-45c1-aef8-b327bdc076e6">

</br>

<img width="1311" alt="Screenshot 2023-08-31 at 11 59 06 AM" src="https://github.com/halfdreamt/Tripartite/assets/31080937/9bda6e5a-785f-4cab-a1b7-ac78f9a5acd8">

## Contributing

Tripartite is a work in progress and only the fundamental ECS system is currently in place. 

## License

[MIT](https://choosealicense.com/licenses/mit/)
