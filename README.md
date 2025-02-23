# Card Reader Display Project

This project is designed to read RFID cards using the RDM6300 module and display the information on a screen.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/card_reader_display.git
    cd card_reader_display
    ```

2. Initialize the project:
    ```sh
    source init.sh
    ```

3. Connect the RDM6300 RFID reader and the display module to your Raspberry Pi as per the wiring diagram provided in the `docs` directory.

## Usage

To run the project, execute the following command:
```sh
python main.py
```

## Credits
Courtesy of [The Mad Tinkerer](https://github.com/mad-tinkerer/python-rdm6300)
- **RDM6300**: The 125KHz RFID reader module used in this project.
Courtesy of [FreeNOVE](https://github.com/Freenove)
- **Display_src**: The source code for handling the display module.
- **RFID_src**: The source code for interfacing with the RFID reader.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.