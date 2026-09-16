from midi.mido_adapter import MidoDeviceProvider
from midi.monitor import MidiMonitor


class Application:
    def __init__(self) -> None:
        self._midi = MidoDeviceProvider()

    def run(self) -> int:
        input_ports = self._midi.input_ports()

        if not input_ports:
            print("MIDI port not found.")
            return 1

        print("MIDI INPUTS")

        for index, port in enumerate(input_ports):
            print(f"[{index}] {port}")

        print()

        selected_index = self._select_input_port(input_ports)

        if selected_index is None:
            return 1

        port_name = input_ports[selected_index]

        midi_input = self._midi.create_input(port_name)

        monitor = MidiMonitor(midi_input)

        print()
        print(f"Connecting: {port_name}")
        print("Waiting MIDI messages...")
        print("Press Ctrl+C to interrupt.")
        print()

        monitor.start()

        return 0

    @staticmethod
    def _select_input_port(
        ports: list[str],
    ) -> int | None:
        if len(ports) == 1:
            return 0

        while True:
            value = input("Select the MIDI port: ")

            try:
                index = int(value)

            except ValueError:
                print("Enter a valid number.")
                continue

            if 0 <= index < len(ports):
                return index

            print("Invalid index.")
```
