# Bloons TD Battles Game (Local Implementation)

This project is a Python-based implementation of a game inspired by Bloons TD Battles, featuring a client-server architecture for networked gameplay. Players strategically place monkeys (towers) to defend against waves of balloons.

## Key Features

* **Client-Server Architecture:** Supports multiplayer gameplay with a dedicated server (`BTD_Server.py`) and multiple clients (`BTD_Client.py`).
* **Balloon Management:**
    * Balloons of varying types (`balloon.py`, `balloon_data.py`) with different health and speed attributes (red, blue, green, yellow).
    * Balloons follow predefined waypoints on the game map.
    * The server controls balloon spawning and sends balloon data to clients.
* **Monkey Towers:**
    * Players can place and upgrade monkey towers (`monkey.py`, `monkey_data.py`) with different ranges and cooldowns.
    * Monkeys target and attack balloons within their range.
    * Clients send monkey placement and upgrade information to the server.
* **Game World:**
    * The game world (`world.py`) manages game state, including player health, money, level progression, and balloon waves.
    * The playground (`playground.py`) handles the game map.
* **User Interface:**
    * Clients use Pygame to render the game and provide a GUI.
    * Buttons (`button.py`) are used for player interaction.
* **Network Communication:**
    * `tcp_by_size.py` handles TCP socket communication, including sending and receiving data with size prefixes to ensure complete message delivery.
    * The server uses threading to manage multiple client connections.

## Modules

* `BTD_Client.py`: Implements the client-side game application using Pygame. Handles user input, rendering, and communication with the server.
* `BTD_Server.py`: Implements the server-side game logic. Manages client connections, game state, balloon spawning, and communication with clients.
* `balloon.py`: Defines the `Balloon` class, which represents the balloons that players must defend against. Includes logic for movement, health, and type.
* `balloon_data.py`: Contains data structures (`BALLOON_DATA`) defining the properties (health, speed) of different balloon types.
* `button.py`: Defines the `Button` class, used to create interactive buttons within the Pygame interface.
* `monkey.py`: Defines the `Monkey` class, representing the towers that players place to attack balloons. Includes logic for targeting, attacking, and upgrading.
* `monkey_data.py`: Contains data structures (`MONKEY_DATA`) defining the properties (range, cooldown) of monkey towers at different upgrade levels.
* `playground.py`: Handles loading and managing the game map image.
* `tcp_by_size.py`: Provides utility functions for sending and receiving data over TCP sockets, ensuring that complete messages are transmitted by prefixing them with their size.
* `world.py`: Defines the `World` class, which manages the overall game state, including level progression, player resources, and balloon spawning.

## How to Run

1.  **Start the Server:**
    Run the server script:
    ```bash
    python BTD_Server.py
    ```

2.  **Start the Client(s):**
    Run the client script for each player:
    ```bash
    python BTD_Client.py
    ```

3.  **Gameplay:**
    * Clients connect to the server.
    * Players place monkeys to defend against incoming balloons.
    * The game progresses through levels, with increasing difficulty.

Further gameplay instructions and specific controls are managed within the client application.
