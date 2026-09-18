from midi.message_type import MidiMessageType

from ampero.protocol.specification import (
    AmperoMiniMidiSpecification,
    MidiCommandMapping,
    MidiCommandSequence,
)

MIDI_CHANNEL = 0

CC_BANK_MSB = 0

CC_EFFECT_1 = 48
CC_EFFECT_2 = 49
CC_EFFECT_3 = 50
CC_EFFECT_4 = 51
CC_EFFECT_5 = 52
CC_EFFECT_6 = 53

def create_reference_specification() -> AmperoMiniMidiSpecification:
    return AmperoMiniMidiSpecification(
        presets_per_bank=10,
        preset_mapping=MidiCommandSequence(
            messages=(
                MidiCommandMapping(
                    message_type=MidiMessageType.CONTROL_CHANGE,
                    channel=MIDI_CHANNEL,
                    control=CC_BANK_MSB,
                ),
                MidiCommandMapping(
                    message_type=MidiMessageType.PROGRAM_CHANGE,
                    channel=MIDI_CHANNEL,
                ),
            )
        ),
        effect_mappings={
            "effect_1": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_1,
            ),
            "effect_2": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_2,
            ),
            "effect_3": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_3,
            ),
            "effect_4": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_4,
            ),
            "effect_5": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_5,
            ),
            "effect_6": MidiCommandMapping(
                message_type=MidiMessageType.CONTROL_CHANGE,
                channel=MIDI_CHANNEL,
                control=CC_EFFECT_6,
            ),
        },
    )